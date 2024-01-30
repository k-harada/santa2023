#!/bin/bash

# SEED=10
# gcloud ai custom-jobs create \
#     --project=kaggle-playground \
#     --region=us-central1 \
#     --display-name="cube-even-seed-${SEED}" \
#     --config=vertex.yaml \
#     --args="solve-even,--seed,${SEED}"

gcloud ai custom-jobs create \
    --project=kaggle-playground \
    --region=us-central1 \
    --display-name="cube-even" \
    --config=vertex.yaml \
    --args="solve-even"
