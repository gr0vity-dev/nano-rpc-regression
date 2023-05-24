#!/bin/bash

display_usage() {
    echo "Usage: $0 <version> [options]"
    echo "Options:"
    echo "  -r, --reset            Perform a reset"
    echo "  -s, --save-ledger      Save the ledger"
    echo "  -l, --restore-ledger   Restore the ledger"
    exit 1
}

# Check if version argument is provided
if [ $# -lt 1 ]; then
    display_usage
fi

# Default values for options
RESET=false
SAVE_LEDGER=false
RESTORE_LEDGER=false

# Parse options
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -r|--reset)
            RESET=true
            shift
            ;;
        -s|--save-ledger)
            SAVE_LEDGER=true
            shift
            ;;
        -l|--restore-ledger)
            RESTORE_LEDGER=true
            shift
            ;;
        *)
            VERSION=$key
            shift
            ;;
    esac
done

# Validate version argument
if [ -z "$VERSION" ]; then
    echo "Error: Version argument is required."
    display_usage
fi

if $RESTORE_LEDGER; then
    mkdir -p nano_nodes/nl_pr1/NanoTest/
    mkdir -p nano_nodes/nl_genesis/NanoTest/
    cp saved_ledger.ldb nano_nodes/nl_pr1/NanoTest/data.ldb
    cp saved_ledger.ldb nano_nodes/nl_genesis/NanoTest/data.ldb
fi

nanomock conf_edit --payload "{\"path\": \"representatives.docker_tag\", \"value\": \"$VERSION\"}"
nanomock create
nanomock down
nanomock create
nanomock start

if $RESET; then
    nanomock reset
    nanomock start
    nanomock init
    nanomock rpc --payload '{"action":"process","json_block":"true","subtype":"send","block":{"type":"state","account":"nano_1ge7edbt774uw7z8exomwiu19rd14io1nocyin5jwpiit3133p9eaaxn74ub","previous":"CE7E7AB0BC9F3D585C3E58E28ED285388B8174A221D1F890489E22768041CBAC","representative":"nano_1ge7edbt774uw7z8exomwiu19rd14io1nocyin5jwpiit3133p9eaaxn74ub","balance":"199000000000000000000000000000000000000","link":"C3567B864AA3380F36B853C73F5AB09BCDEFBB323F2DEED8BAE4280CCA277674","link_as_account":"nano_3itphg56oasr3wudiny99xfd38yfxyxm6hsfxuedos3a3m74gxmn4njzx5np","signature":"198B8E75A4E937E7DD9AF9A303FA1AE729D34566DD384456ADFC067F05B681B99A58DB1B6B0A0445AA155B98D4BD2921881D8EB53795A3ED629463FB7DADF50B","work":"6602d6f343de01f3"}}' --nodes nl_pr1
    nanomock restart
    sleep 5
fi

if $SAVE_LEDGER; then
    cp nano_nodes/nl_pr1/NanoTest/data.ldb saved_ledger.ldb
fi

nanomock status
