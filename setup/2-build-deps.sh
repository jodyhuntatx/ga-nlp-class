#!/bin/bash
main() {
  install_cuda_toolkit
#  build_llama_cpp
#  download_model_from_hf
}

#########################
install_cuda_toolkit() {
  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
  sudo dpkg -i cuda-keyring_1.1-1_all.deb
  sudo apt-get update
  sudo apt-get -y install cuda
}

#########################
build_llama_cpp() {
  echo
  echo "Runtime ~20:00"
  time CMAKE_ARGS="-DGGML_CUDA=on -DCUDA_PATH=/usr/local/cuda-12.2 -DCUDAToolkit_ROOT=/usr/local/cuda-12.2 -DCUDAToolkit_INCLUDE_DIR=/usr/local/cuda-12/include -DCUDAToolkit_LIBRARY_DIR=/usr/local/cuda-12.2/lib64" FORCE_CMAKE=1 pip install llama-cpp-python --no-cache-dir
}

#########################
download_model_from_hf() {
#  model_url="https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main"
#  model_name="llama-2-13b-chat.Q5_K_M.gguf"
  model_url="https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main"
  model_name="mistral-7b-instruct-v0.2.Q5_K_M.gguf"
  wget $model_url/$model_name
  mv $model_name ~/models
}

main "$@"
