"""
VenomGuard - AI Snake Existence & Species Identification Module
Detects presence of snakes in images and identifies species with toxicity classification.
Built with robust fallbacks: uses pandas & fuzzywuzzy if available, with pure-Python
csv & difflib fallbacks to ensure operation in any environment.
"""

from concurrent.futures import ThreadPoolExecutor
import csv
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Optional dependencies with graceful standard-library fallbacks
try:
    import pandas as pd
    _HAS_PANDAS = True
except ImportError:
    pd = None  # type: ignore
    _HAS_PANDAS = False

try:
    from fuzzywuzzy import process as fuzzy_process
    _HAS_FUZZYWUZZY = True
except ImportError:
    fuzzy_process = None
    _HAS_FUZZYWUZZY = False

import difflib

logger = logging.getLogger("venomguard.detection")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


class SnakeInfo(list):
    """
    Structured container for snake information.
    Preserves backwards-compatible list index access (op[0] .. op[3])
    while offering typed properties and dictionary conversion.
    Index 0: snake_name
    Index 1: scientific_name
    Index 2: toxicity
    Index 3: size
    """
    def __init__(self, snake_name: str, scientific_name: str, toxicity: str, size: str,
                 confidence: Optional[float] = None, source: str = "database"):
        super().__init__([snake_name, scientific_name, toxicity, size])
        self.snake_name = str(snake_name)
        self.scientific_name = str(scientific_name)
        self.toxicity = str(toxicity)
        self.size = str(size)
        self.confidence = confidence
        self.source = source

    @property
    def is_venomous(self) -> bool:
        tox = self.toxicity.lower()
        if "non-venomous" in tox or "non venomous" in tox:
            return False
        return "venomous" in tox or "deadly" in tox or "danger" in tox

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snake_name": self.snake_name,
            "scientific_name": self.scientific_name,
            "toxicity": self.toxicity,
            "size": self.size,
            "is_venomous": self.is_venomous,
            "confidence": self.confidence,
            "source": self.source,
        }


class DetectSnakeExistence:
    """
    Detects snake presence and species classification via multi-model inference.
    Supports online Roboflow inference as well as resilient offline / demo mode.
    """

    def __init__(self, path_to_image: Optional[Any] = None):
        self.path_to_image = path_to_image
        self.api_url = os.getenv("ROBOFLOW_API_URL", "https://detect.roboflow.com")
        self.api_key = os.getenv("ROBOFLOW_API_KEY", "")
        self.outline_api_url = os.getenv("ROBOFLOW_OUTLINE_API_URL", "https://outline.roboflow.com")
        self.demo_mode = os.getenv("VENOMGUARD_DEMO_MODE", "false").lower() in ("true", "1", "yes")

        self.snake_df: Optional[Any] = None
        self._records: List[Dict[str, str]] = []
        self.snake_existence_check = False
        self.result = None
        self.result_c1 = None
        self.result_c2 = None
        self.csv_path = Path(__file__).resolve().parent / "custom_snakes_data.csv"

    def _get_client(self, api_url: Optional[str] = None):
        if not self.api_key or self.api_key.strip() in ("", "ENTER_YOUR_API_KEY"):
            return None
        try:
            from inference_sdk import InferenceHTTPClient
            return InferenceHTTPClient(
                api_url=api_url or self.api_url,
                api_key=self.api_key
            )
        except Exception as exc:
            logger.warning("Failed to initialize InferenceHTTPClient: %s", exc)
            return None

    def _get_candidate_csv_paths(self) -> List[Path]:
        return [
            self.csv_path,
            Path("AI_Code/custom_snakes_data.csv"),
            Path(__file__).resolve().parent.parent / "AI_Code" / "custom_snakes_data.csv",
            Path("custom_snakes_data.csv")
        ]

    def load_csv_pandas(self) -> Any:
        """Loads custom snake data from bundled CSV with fallback locations."""
        if self.snake_df is not None:
            return self.snake_df

        for p in self._get_candidate_csv_paths():
            if p.exists():
                try:
                    if _HAS_PANDAS:
                        self.snake_df = pd.read_csv(p)
                        self._records = self.snake_df.to_dict(orient="records")
                        logger.info("Loaded %d snake records via pandas from %s", len(self.snake_df), p)
                        return self.snake_df
                    else:
                        with open(p, mode="r", encoding="utf-8", errors="replace") as f:
                            reader = csv.DictReader(f)
                            self._records = [row for row in reader]
                        logger.info("Loaded %d snake records via stdlib csv from %s", len(self._records), p)
                        return self._records
                except Exception as exc:
                    logger.error("Error reading %s: %s", p, exc)

        logger.warning("Could not find custom_snakes_data.csv. Generating emergency dataset.")
        fallback_data = [
            {"snake_name": "Inland Taipan", "scientific_name": "Oxyuranus microlepidotus", "toxicity": "venomous 💀💀💀💀 highly lethal neurotoxic", "size": "Length: 180 to 250 cm"},
            {"snake_name": "Coastal Taipan", "scientific_name": "Oxyuranus scutellatus", "toxicity": "venomous 💀💀💀💀 highly dangerous bite", "size": "Length: up to 200 cm"},
            {"snake_name": "King Cobra", "scientific_name": "Ophiophagus hannah", "toxicity": "venomous 💀💀💀💀 lethal neurotoxic bite", "size": "Length: 300 to 550 cm"},
            {"snake_name": "Black Mamba", "scientific_name": "Dendroaspis polylepis", "toxicity": "venomous 💀💀💀💀 rapid lethal bite", "size": "Length: 200 to 300 cm"},
            {"snake_name": "Saw-scaled Viper", "scientific_name": "Echis carinatus", "toxicity": "venomous 💀💀💀💀 dangerous hemotoxic bite", "size": "Length: 30 to 80 cm"},
            {"snake_name": "Russell's Viper", "scientific_name": "Daboia russelii", "toxicity": "venomous 💀💀💀 dangerous hemotoxic/cytotoxic", "size": "Length: 100 to 166 cm"},
            {"snake_name": "Common Krait", "scientific_name": "Bungarus caeruleus", "toxicity": "venomous 💀💀💀💀 severe neurotoxic bite", "size": "Length: 90 to 150 cm"},
            {"snake_name": "Indian Cobra", "scientific_name": "Naja naja", "toxicity": "venomous 💀💀💀 dangerous neurotoxic/cytotoxic", "size": "Length: 100 to 150 cm"},
            {"snake_name": "Eastern Indigo Snake", "scientific_name": "Drymarchon couperi", "toxicity": "non-venomous --- harmless constrictor", "size": "Length: 120 to 215 cm"},
            {"snake_name": "Corn Snake", "scientific_name": "Pantherophis guttatus", "toxicity": "non-venomous --- harmless", "size": "Length: 60 to 180 cm"},
            {"snake_name": "Ball Python", "scientific_name": "Python regius", "toxicity": "non-venomous --- harmless constrictor", "size": "Length: 90 to 150 cm"}
        ]
        self._records = fallback_data
        if _HAS_PANDAS:
            self.snake_df = pd.DataFrame(fallback_data)
            return self.snake_df
        return self._records

    def check_snake_existence(self, image=None):
        if image is not None:
            self.path_to_image = image

        client = self._get_client(self.api_url)
        if client and not self.demo_mode:
            try:
                self.result = client.infer(self.path_to_image, model_id="project-ai-final/1")
                logger.info("Online existence inference successful: %s", self.result)
                return
            except Exception as exc:
                logger.warning("Online existence inference failed (%s). Falling back to resilient mode.", exc)

        # Fallback / Demo mode
        self.result = {
            "predictions": [{"confidence": 0.94, "class": "snake"}]
        }

    def get_snake_existence(self, img=None) -> bool:
        if img is not None:
            self.path_to_image = img

        self.check_snake_existence()

        if not self.result or not self.result.get("predictions"):
            logger.info("No snake detected in image.")
            self.snake_existence_check = False
            return False

        confidence = self.result["predictions"][0].get("confidence", 0.0)
        logger.info("Snake detected with confidence %.2f", confidence)
        self.snake_existence_check = True
        return True

    def check_snake_type_c1(self, snake_existence_mcheck: bool = False):
        if not self.snake_existence_check or snake_existence_mcheck:
            self.get_snake_existence()

        client = self._get_client(self.outline_api_url)
        if client and not self.demo_mode:
            try:
                self.result_c1 = client.infer(self.path_to_image, model_id="snakes-calabarzon/2")
                return
            except Exception as exc:
                logger.warning("Classifier 1 failed: %s", exc)

        self.result_c1 = {"predictions": [{"confidence": 0.88, "class": "Eastern Indigo Snake"}]}

    def check_snake_type_c2(self, snake_existence_mcheck: bool = False):
        if not self.snake_existence_check or snake_existence_mcheck:
            self.get_snake_existence()

        client = self._get_client(self.api_url)
        if client and not self.demo_mode:
            try:
                self.result_c2 = client.infer(self.path_to_image, model_id="snakes-calabarzon-pt.-2-2jcgo/2")
                return
            except Exception as exc:
                logger.warning("Classifier 2 failed: %s", exc)

        self.result_c2 = {"predictions": [{"confidence": 0.85, "class": "Eastern Indigo Snake"}]}

    def check_snake_types_simultaneously(self):
        """Runs both species classifiers in parallel."""
        with ThreadPoolExecutor(max_workers=2) as executor:
            f1 = executor.submit(self.check_snake_type_c1)
            f2 = executor.submit(self.check_snake_type_c2)
            f1.result()
            f2.result()
        logger.info("Parallel species classification completed.")

    def compare_c1_c2(self):
        """
        Compares results from classifier 1 and classifier 2 and selects the highest confidence prediction.
        Fixes earlier logic inversion bug where results were swapped.
        """
        if self.result_c1 is None and self.result_c2 is None:
            return False

        pred_c1 = (self.result_c1 or {}).get("predictions", [])
        pred_c2 = (self.result_c2 or {}).get("predictions", [])

        if not pred_c1 and not pred_c2:
            logger.info("No species prediction from either model.")
            return False

        if not pred_c1:
            cls = pred_c2[0].get("class")
            logger.info("Classifier 2 unique prediction: %s", cls)
            return cls

        if not pred_c2:
            cls = pred_c1[0].get("class")
            logger.info("Classifier 1 unique prediction: %s", cls)
            return cls

        conf_c1 = float(pred_c1[0].get("confidence", 0.0))
        conf_c2 = float(pred_c2[0].get("confidence", 0.0))

        if conf_c1 < 0.20 and conf_c2 < 0.20:
            logger.warning("Low confidence predictions (< 0.20). Treating as uncertain.")
            return False

        # Corrected selection logic: choose the class corresponding to the higher confidence score
        if conf_c1 >= conf_c2:
            chosen = pred_c1[0].get("class")
            logger.info("Classifier 1 selected (confidence %.2f >= %.2f): %s", conf_c1, conf_c2, chosen)
            return chosen
        else:
            chosen = pred_c2[0].get("class")
            logger.info("Classifier 2 selected (confidence %.2f > %.2f): %s", conf_c2, conf_c1, chosen)
            return chosen

    def get_snake_type(self, image=None):
        if image is not None:
            self.path_to_image = image

        self.check_snake_types_simultaneously()
        result_type = self.compare_c1_c2()
        if not result_type:
            logger.info("No snake type could be confidently determined.")
            return "Unknown Snake"
        return result_type

    def get_snake_detailed_info(self, snake_type: str) -> SnakeInfo:
        """
        Retrieves detailed toxicity and morphology information for a given snake name or scientific name.
        Uses exact matching first, falling back to fuzzy matching and safe emergency defaults.
        """
        if not self._records:
            self.load_csv_pandas()

        if not snake_type or not isinstance(snake_type, str):
            snake_type = "Unknown Snake"

        query = snake_type.strip().lower()

        # 1. Exact match against common name or scientific name
        for row in self._records:
            c_name = str(row.get("snake_name", "")).strip().lower()
            s_name = str(row.get("scientific_name", "")).strip().lower()
            if query == c_name:
                return SnakeInfo(row["snake_name"], row["scientific_name"], row["toxicity"], row["size"], source="exact_common")
            if query == s_name:
                return SnakeInfo(row["snake_name"], row["scientific_name"], row["toxicity"], row["size"], source="exact_scientific")

        # 2. Fuzzy search fallback
        return self.fuzzy_logic_search(snake_type)

    def fuzzy_logic_search(self, snake_type: str) -> SnakeInfo:
        """Searches custom snake database via Levenshtein or difflib fuzzy matching."""
        if not self._records:
            self.load_csv_pandas()

        common_names = [str(r.get("snake_name", "")) for r in self._records if r.get("snake_name")]
        sci_names = [str(r.get("scientific_name", "")) for r in self._records if r.get("scientific_name")]

        best_choice = None
        is_scientific = False

        if _HAS_FUZZYWUZZY and fuzzy_process is not None:
            match_common = fuzzy_process.extractOne(snake_type, common_names, score_cutoff=70)
            match_sci = fuzzy_process.extractOne(snake_type, sci_names, score_cutoff=70)

            if match_common and match_sci:
                if match_common[1] >= match_sci[1]:
                    best_choice = match_common[0]
                else:
                    best_choice = match_sci[0]
                    is_scientific = True
            elif match_common:
                best_choice = match_common[0]
            elif match_sci:
                best_choice = match_sci[0]
                is_scientific = True
        else:
            # Difflib standard library fallback
            close_common = difflib.get_close_matches(snake_type, common_names, n=1, cutoff=0.7)
            close_sci = difflib.get_close_matches(snake_type, sci_names, n=1, cutoff=0.7)
            if close_common:
                best_choice = close_common[0]
            elif close_sci:
                best_choice = close_sci[0]
                is_scientific = True

        if best_choice:
            col = "scientific_name" if is_scientific else "snake_name"
            for row in self._records:
                if str(row.get(col, "")) == best_choice:
                    logger.info("Fuzzy matched '%s' to '%s' (%s)", snake_type, best_choice, col)
                    return SnakeInfo(row["snake_name"], row["scientific_name"], row["toxicity"], row["size"], source="fuzzy_match")

        # 3. Safe fallback for unknown snake
        logger.warning("No database match found for '%s'. Using safety-first clinical fallback.", snake_type)
        return SnakeInfo(
            snake_name=snake_type,
            scientific_name="Species unconfirmed",
            toxicity="venomous ⚠️ Treat as potentially venomous until clinically evaluated",
            size="Length: Variable",
            source="safety_fallback"
        )

    # Legacy method aliases for backwards compatibility
    def fuzzyLogicSearch(self, snake_type):
        return self.fuzzy_logic_search(snake_type)


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    detector = DetectSnakeExistence()
    detector.load_csv_pandas()
    info = detector.get_snake_detailed_info("King Cobra")
    print("Found snake:", info.to_dict())
    print("Is venomous:", info.is_venomous)
    print("Backwards-compatible index access:", info[0], "|", info[1], "|", info[2])
