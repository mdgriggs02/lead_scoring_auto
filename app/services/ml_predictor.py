import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Optional
import os
from pathlib import Path
import json
from datetime import datetime, timedelta

class LeadPredictor:
    def __init__(self):
        self.model: Optional[RandomForestClassifier] = None
        self.scaler: Optional[StandardScaler] = None
        self.model_path = Path("app/models/lead_predictor.joblib")
        self.scaler_path = Path("app/models/scaler.joblib")
        self.version = "1.0.0"
        self.metadata_path = Path("app/models/metadata.json")
        self._load_model()
        self._load_metadata()

    def _load_model(self):
        """Load the trained model and scaler if they exist"""
        try:
            if self.model_path.exists() and self.scaler_path.exists():
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
        except Exception as e:
            print(f"Error loading model: {str(e)}")

    def _load_metadata(self):
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "version": self.version,
                "training_date": None,
                "num_samples": 0,
                "performance_metrics": {}
            }

    def _prepare_features(self, metrics: Dict) -> np.ndarray:
        """Convert engagement metrics to feature array with additional features"""
        basic_features = np.array([
            metrics["website_visits"],
            metrics["time_on_site"],
            metrics["pages_viewed"],
            metrics["downloaded_resources"],
            metrics["email_interactions"]
        ])
        
        # Add derived features
        engagement_rate = metrics["pages_viewed"] / max(metrics["website_visits"], 1)
        avg_time_per_visit = metrics["time_on_site"] / max(metrics["website_visits"], 1)
        
        features = np.concatenate([
            basic_features,
            [engagement_rate, avg_time_per_visit]
        ]).reshape(1, -1)
        
        if self.scaler:
            features = self.scaler.transform(features)
        
        return features

    async def predict_conversion(self, metrics: Dict) -> float:
        """Predict conversion probability for a lead"""
        if not self.model:
            # Return a heuristic-based score if model isn't trained
            return self._calculate_heuristic_score(metrics)

        features = self._prepare_features(metrics)
        probabilities = self.model.predict_proba(features)
        return float(probabilities[0][1])  # Probability of conversion

    def _calculate_heuristic_score(self, metrics: Dict) -> float:
        """Fallback heuristic scoring when model isn't trained"""
        weights = {
            "website_visits": 0.2,
            "time_on_site": 0.2,
            "pages_viewed": 0.2,
            "downloaded_resources": 0.25,
            "email_interactions": 0.15
        }
        
        normalized_metrics = {
            "website_visits": min(metrics["website_visits"] / 10, 1),
            "time_on_site": min(metrics["time_on_site"] / 300, 1),
            "pages_viewed": min(metrics["pages_viewed"] / 5, 1),
            "downloaded_resources": min(metrics["downloaded_resources"] / 2, 1),
            "email_interactions": min(metrics["email_interactions"] / 3, 1)
        }
        
        score = sum(normalized_metrics[k] * weights[k] for k in weights)
        return score

    async def train(self, training_data: List[Dict], labels: List[int]):
        """Train the model with historical data"""
        if len(training_data) < 10:
            raise ValueError("Insufficient training data")

        # Prepare features
        X = np.array([[
            lead["website_visits"],
            lead["time_on_site"],
            lead["pages_viewed"],
            lead["downloaded_resources"],
            lead["email_interactions"]
        ] for lead in training_data])

        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42
        )
        self.model.fit(X_scaled, labels)

        # Save model and scaler
        os.makedirs(self.model_path.parent, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)

        # Calculate and store performance metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        y_pred = self.model.predict(X_scaled)
        
        self.metadata.update({
            "training_date": datetime.utcnow().isoformat(),
            "num_samples": len(training_data),
            "performance_metrics": {
                "accuracy": float(accuracy_score(labels, y_pred)),
                "precision": float(precision_score(labels, y_pred)),
                "recall": float(recall_score(labels, y_pred))
            }
        })

        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def needs_retraining(self) -> bool:
        """Check if model needs retraining"""
        if not self.metadata["training_date"]:
            return True
            
        last_training = datetime.fromisoformat(self.metadata["training_date"])
        return datetime.utcnow() - last_training > timedelta(days=7) 