source ../venv/bin/activate
source ./envs.bash

BOOTLEG_TRAIN_DATA_DIR=$BOOTLEG_DATA_DIR/output/full_wiki_0_-1_final
BASE_CONFIG=$BOOTLEG_CONFIGS_DIR/base_config.yaml
BOOTLEG_ENTITYDB_DIR=$BOOTLEG_TRAIN_DATA_DIR/entity_db

cp $BASE_CONFIG /tmp/base_config.yaml
sed -i "s|BOOTLEG_LOGS_DIR|$BOOTLEG_LOGS_DIR|g" /tmp/base_config.yaml
sed -i "s|BOOTLEG_TRAIN_DATA_DIR|$BOOTLEG_TRAIN_DATA_DIR|g" /tmp/base_config.yaml
sed -i "s|BOOTLEG_BERT_CACHE_DIR|$BOOTLEG_BERT_CACHE_DIR|g" /tmp/base_config.yaml
sed -i "s|BOOTLEG_ENTITYDB_DIR|$BOOTLEG_ENTITYDB_DIR|g" /tmp/base_config.yaml
sed -i "s|BOOTLEG_BERT_MODEL|$BOOTLEG_BERT_MODEL|g" /tmp/base_config.yaml
sed -i "s|BOOTLEG_PROCESS_COUNT|$BOOTLEG_PROCESS_COUNT|g" /tmp/base_config.yaml

cat /tmp/base_config.yaml
echo ''
echo 'Starting to train...'
echo ''
python3 $BOOTLEG_CODE_DIR/bootleg/run.py --config_script /tmp/base_config.yaml
