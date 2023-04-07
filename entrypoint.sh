#!/bin/sh

cd $BYTEWAX_WORKDIR
. /venv/bin/activate
python -m bytewax.run $BYTEWAX_PYTHON_FILE_PATH

echo 'Process ended.'

if [ "$BYTEWAX_KEEP_CONTAINER_ALIVE" = true ]
then
    echo 'Keeping container alive...';
    while :; do sleep 1; done
fi
