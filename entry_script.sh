#!/bin/sh
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  exec /usr/local/bin/aws-lambda-rie /usr/local/bin/python -m awslambdaric $@
  # exec /usr/local/bin/aws-lambda-rie /usr/bin/python3 -m awslambdaric $@
else
  exec /usr/local/bin/python -m awslambdaric $@
  # exec /usr/bin/python3 -m awslambdaric $@
fi     


# ============================================================================== Below is for self hosting ============================================================================== #

# # supertokens list
# # echo "$(ls /usr/lib/supertokens/webserver-temp/)"
# echo "$(ls -la /tmp)"
# STL=$(/tmp/supertokens list)
# if [ "$STL" = "No SuperTokens instances running." ]; then
#   # chmod -R 777 /usr/lib/supertokens
#   /tmp/supertokens start --with-config=/usr/src/supertokens/config.yaml
#   # echo "$(ls /usr/lib/supertokens/webserver-temp/)"
#   # supertokens start --with-config=/tmp/supertokens/config.yaml
# fi

# service docker start
# systemctl status docker
# docker run -p 3567:3567 -d registry.supertokens.io/supertokens/supertokens-postgresql