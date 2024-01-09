# syntax=docker/dockerfile:1

FROM biocontainers/blast:v2.2.31_cv2

USER root
RUN apt-get update && (apt-get install -t buster-backports -y python3-biopython || apt-get install -y python3-biopython) && apt-get clean && apt-get purge && rm -rf /var/lib/apt/lists/* /tmp/*
USER biodocker
