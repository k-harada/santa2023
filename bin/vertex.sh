#!/bin/bash

for i in {0..9}; do
    SEED=$i

    gcloud ai custom-jobs create \
    --project=kaggle-playground \
    --region=us-central1 \
    --display-name="cube-seed-${SEED}" \
    --config=vertex.yaml \
    --args="solve,--seed,${SEED}"
done
