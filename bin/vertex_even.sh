#!/bin/bash

for i in {1..9}; do
    SEED=$i

    gcloud ai custom-jobs create \
    --project=kaggle-playground \
    --region=us-central1 \
    --display-name="cube-even-seed-${SEED}" \
    --config=vertex.yaml \
    --args="solve-even,--seed,${SEED}"
done
