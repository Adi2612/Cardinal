FROM gcr.io/deeplearning-platform-release/base-cpu

WORKDIR /src

RUN conda create -n cardinal-env python=3.7 pip

EXPOSE 6534

CMD ["/bin/bash", "main.sh"]