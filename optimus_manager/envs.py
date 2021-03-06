VERSION = "1.3.2"
from optimus_manager.pci import get_available_igpu

SOCKET_PATH = "/tmp/optimus-manager"
SOCKET_TIMEOUT = 1.0

PERSISTENT_VARS_FOLDER_PATH = "/var/lib/optimus-manager/persistent"
ACPI_CALL_STRING_VAR_PATH = "%s/acpi_call_strings.json" % PERSISTENT_VARS_FOLDER_PATH
TEMP_CONFIG_PATH_VAR_PATH = "%s/temp_conf_path" % PERSISTENT_VARS_FOLDER_PATH

TMP_VARS_FOLDER_PATH = "/var/lib/optimus-manager/tmp"
LAST_ACPI_CALL_STATE_VAR = "%s/last_acpi_call_state" % TMP_VARS_FOLDER_PATH
STATE_FILE_PATH = "%s/state.json" % TMP_VARS_FOLDER_PATH
USER_CONFIG_COPY_PATH = "%s/config_copy.conf" % TMP_VARS_FOLDER_PATH
CURRENT_DAEMON_RUN_ID = "%s/daemon_run_id" % TMP_VARS_FOLDER_PATH

XORG_CONF_PATH = "/etc/X11/xorg.conf.d/10-optimus-manager.conf"

DEFAULT_CONFIG_PATH = "/usr/share/optimus-manager.conf"
USER_CONFIG_PATH = "/etc/optimus-manager/optimus-manager.conf"

EXTRA_XORG_OPTIONS_PATHS = {
    "intel": "/etc/optimus-manager/xorg-intel.conf",
    "nvidia": "/etc/optimus-manager/xorg-nvidia.conf",
    "hybrid-intel": "/etc/optimus-manager/xorg-hybrid.conf",
    "hybrid-amd": "/etc/optimus-manager/xorg-hybrid.conf",
    "amd": "/etc/optimus-manager/xorg-amd.conf"
}

XSETUP_SCRIPTS_PATHS = {
    "intel": "/etc/optimus-manager/xsetup-intel.sh",
    "nvidia": "/etc/optimus-manager/xsetup-nvidia.sh",
    "hybrid-intel": "/etc/optimus-manager/xsetup-hybrid.sh",
    "hybrid-amd": "/etc/optimus-manager/xsetup-hybrid.sh",
    "amd": "/etc/optimus-manager/xsetup-amd.sh"
}

NVIDIA_MANUAL_ENABLE_SCRIPT_PATH = "/etc/optimus-manager/nvidia-enable.sh"
NVIDIA_MANUAL_DISABLE_SCRIPT_PATH = "/etc/optimus-manager/nvidia-disable.sh"

LOG_DIR_PATH = "/var/log/optimus-manager"
