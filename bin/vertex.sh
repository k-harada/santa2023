#!/bin/bash

PUZZLE_ID=281

for i in {6..10}; do
    SEED="${i}"
    gcloud ai custom-jobs create \
        --project=kaggle-playground \
        --region=us-central1 \
        --display-name="cube-id-${PUZZLE_ID}-seed-${SEED}" \
        --config=vertex.yaml \
        --args="solve,--seed,${SEED},--puzzle-id,${PUZZLE_ID}"
done
