#!/bin/bash

if [ $# -eq 1 ]; then
	export SDO_ROOT=$1
	export SCRIPT_PATH=$SDO_ROOT/utils
	#$SCRIPT_PATH/val_report_gen.py  $SDO_ROOT   ecdsa256    ccm

	##  Python_Script     SDO_DIR       DA     AES_MODE
	$SCRIPT_PATH/val_report_gen.py  $SDO_ROOT   ecdsa256     ccm
	$SCRIPT_PATH/val_report_gen.py  $SDO_ROOT   ecdsa256     gcm
	$SCRIPT_PATH/val_report_gen.py  $SDO_ROOT   ecdsa384     ccm
	$SCRIPT_PATH/val_report_gen.py  $SDO_ROOT   ecdsa384     gcm
else
	echo "Usage: bash /path/to/valgrind.sh /path/to/client_sdk_fidoiot"
	exit 0
fi
# export SDO_ROOT=$HOME/package_fdo_1.0/client-sdk-fidoiot
# export SAFESTRING_ROOT=$HOME/package_fdo_1.0/safestringlib/
# export TINYCBOR_ROOT=$HOME/package_fdo_1.0/tinycbor/

