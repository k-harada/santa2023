#!/bin/bash

PUZZLE_ID=0

for i in {1..20}; do
    SEED="${i}"
    gcloud ai custom-jobs create \
        --project=kaggle-playground \
        --region=us-central1 \
        --display-name="cube-id-${PUZZLE_ID}-seed-${SEED}" \
        --config=vertex.yaml \
        --args="solve,--seed,${SEED},--puzzle-id,${PUZZLE_ID}"
done
