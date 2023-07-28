docker buildx build -f "{}" --push \
            --build-arg GIT_ENV="${GIT_ENV}" \
            --build-arg USE_DEFAULT_GIT="${USE_DEFAULT_GIT}" \
            --progress=plain --no-cache \
            --platform {} \
            {}.