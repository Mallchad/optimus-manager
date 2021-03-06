import sys
from .. import checks
from ..xorg import is_there_a_default_xorg_conf_file, is_there_a_MHWD_file
from .. import sessions
from .utils import ask_confirmation
from ..pci import get_available_igpu


def run_switch_checks(config, requested_mode):

    _check_elogind_active()
    _check_daemon_active()
    _check_power_switching(config)
    _check_bbswitch_module(config)
    _check_nvidia_module(requested_mode)
    _check_patched_GDM()
    _check_igpu(requested_mode)
    _check_wayland()
    _check_bumblebeed()
    _check_xorg_conf()
    _check_MHWD_conf()
    _check_intel_xorg_module(config, requested_mode)
    _check_amd_xorg_module(config, requested_mode)
    _check_number_of_sessions()


def _check_elogind_active():

    if not checks.is_elogind_active() and not checks._detect_init_system(init="systemd"):
        print("The Elogind service was not detected but is required to use optimus-manager, please install, enable and start it.")
        sys.exit(1)


def _check_daemon_active():

    if not checks.is_daemon_active():
        print("The optimus-manager service is not running. Please enable and start it with :\n")
        if checks._detect_init_system(init="openrc"):
            print("sudo rc-service enable optimus-manager\n"
                  "sudo rc-service start optimus-manager\n")
        elif checks._detect_init_system(init="runit-void"):
            print("sudo ln -s /etc/sv/optimus-manager /var/service\n")
        elif checks._detect_init_system(init="runit-artix"):    
            print("sudo ln -s /etc/runit/sv/optimus-manager /run/runit/service\n")
        elif checks._detect_init_system(init="systemd"):
            print("sudo systemctl enable optimus-manager\n"
                  "sudo systemctl start optimus-manager\n")
        elif checks._detect_init_system(init="s6"):
            print("sudo s6-rc-bundle-update add default optimus-manager\n"
                  "sudo s6-rc -u change optimus-mnanager\n")
        else:
            print("ERROR: unsupported init system detected!")
        sys.exit(1)

def _check_power_switching(config):

    if config["optimus"]["switching"] == "none" and config["optimus"]["pci_power_control"] == "no":
        print("WARNING : no power management option is currently enabled (this is the default since v1.2)."
              " Switching between GPUs will work but you will likely experience poor battery life.\n"
              "Follow instructions at https://github.com/Askannz/optimus-manager/wiki/A-guide--to-power-management-options"
              " to enable power management.\n"
              "If you have already enabled the new Runtime D3 power management inside the Nvidia driver (for Turing+ GPU + Coffee Lake+ CPU),"
              " you can safely ignore this warning.\n")

def _check_bbswitch_module(config):

    if config["optimus"]["switching"] == "bbswitch" and not checks.is_module_available("bbswitch"):
        print("WARNING : bbswitch is enabled in the configuration file but the bbswitch module does"
              " not seem to be available for the current kernel. Power switching will not work.\n"
              "You can install bbswitch for the default kernel with \"sudo pacman -S bbswitch\" or"
              " for all kernels with \"sudo pacman -S bbswitch-dkms\".\n")

def _check_nvidia_module(requested_mode):

    if requested_mode == "nvidia" and not checks.is_module_available("nvidia"):
        print("WARNING : the nvidia module does not seem to be available for the current kernel."
              " It is likely the Nvidia driver was not properly installed. GPU switching will probably fail,\n"
              " continue anyway ? (y/N)")

        confirmation = ask_confirmation()

        if not confirmation:
            sys.exit(0)

def _check_patched_GDM():

    try:
        dm_name = checks.get_current_display_manager()
    except checks.CheckError as e:
        print("ERROR : cannot get current display manager name : %s" % str(e))
        return

    if dm_name == "gdm" and not checks.using_patched_GDM():
        print("WARNING : It does not seem like you are using a version of the Gnome Display Manager (GDM)"
              " that has been patched for Prime switching. Follow instructions at https://github.com/Askannz/optimus-manager"
              " to install a patched version. Without a patched GDM version, GPU switching will likely fail.\n"
              "Continue anyway ? (y/N)")

        confirmation = ask_confirmation()

        if not confirmation:
            sys.exit(0)

def _check_wayland():

    try:
        wayland_session_present = sessions.is_there_a_wayland_session()
    except sessions.SessionsError as e:
        print("ERROR : cannot check for Wayland session : %s" % str(e))
        return

    if wayland_session_present:
        print("WARNING : there is at least one Wayland session running on this computer."
              " Wayland is not supported by this optimus-manager, so GPU switching may fail.\n"
              "Continue anyway ? (y/N)")

        confirmation = ask_confirmation()

        if not confirmation:
            sys.exit(0)

def _check_bumblebeed():

    if checks.is_bumblebeed_service_active():
        print("WARNING : The Bumblebee service (bumblebeed.service) is running, and this can interfere with optimus-manager."
              " Before attempting a GPU switch, it is recommended that you disable this service (sudo systemctl disable bumblebeed.service)"
              " then REBOOT your computer.\n"
              "Ignore this warning and proceed with GPU switching now ? (y/N)")

        confirmation = ask_confirmation()

        if not confirmation:
            sys.exit(0)

def _check_xorg_conf():

    if is_there_a_default_xorg_conf_file():
        print("WARNING : Found a Xorg config file at /etc/X11/xorg.conf. If you did not"
              " create it yourself, it was likely generated by your distribution or by an Nvidia utility.\n"
              "This file may contain hard-coded GPU configuration that could interfere with optimus-manager,"
              " so it is recommended that you delete it before proceeding.\n"
              "Ignore this warning and proceed with GPU switching ? (y/N)")

        confirmation = ask_confirmation()

        if not confirmation:
            sys.exit(0)

def _check_MHWD_conf():

    if is_there_a_MHWD_file():
        print("WARNING : Found a Xorg config file at /etc/X11/xorg.conf.d/90-mhwd.conf that was auto-generated"
              " by the Manjaro driver utility (MHWD). This will likely interfere with GPU switching, so"
              " optimus-manager will delete this file automatically if you proceded with GPU switching.\n"
              "Proceed ? (y/N)")

        confirmation = ask_confirmation()

        if not confirmation:
            sys.exit(0)

def _check_intel_xorg_module(config, requested_mode):

    if requested_mode == "intel" and config["intel"]["driver"] == "intel" and not checks.is_xorg_intel_module_available():
        print("WARNING : The Xorg driver \"intel\" is selected in the configuration file but this driver is not installed."
              " optimus-manager will default to the \"modesetting\" driver instead. You can install the \"intel\" driver from"
              " the package \"xf86-video-intel.\"\n"
              "Continue ? (y/N)")

        confirmation = ask_confirmation()

        if not confirmation:
            sys.exit(0)

def _check_amd_xorg_module(config, requested_mode):

    if requested_mode == "amd" and config["amd"]["driver"] == "amdgpu" and not checks.is_xorg_amd_module_available():
        print("WARNING : The Xorg driver \"amdgpu\" is selected in the configuration file but this driver is not installed."
              " optimus-manager will default to the \"modesetting\" driver instead. You can install the \"amdgpu\" driver from"
              " the package \"xf86-video-amdgpu\".\n"
              "Continue ? (y/N)")

        confirmation = _ask_confirmation()

        if not confirmation:
            sys.exit(0)

def _check_igpu(requested_mode):

    detected_igpu = get_available_igpu()

    if requested_mode in ["amd", "hybrid-amd"] and detected_igpu == "intel":
        print("ERROR: No AMD iGPU found!\n"
              "Cannot continue!")
        sys.exit(0)

    elif requested_mode in ["intel", "hybrid-intel"] and detected_igpu == "amd":
        print("ERROR: No Intel GPU found!\n"
              "Cannot continue!")
        sys.exit(0)

def _check_number_of_sessions():

    nb_desktop_sessions = sessions.get_number_of_desktop_sessions(ignore_gdm=True)

    if nb_desktop_sessions > 1:
        print("WARNING : There are %d other desktop sessions open. The GPU switch will not become effective until you have manually"
              " logged out from ALL desktop sessions.\n"
              "Continue ? (y/N)" % (nb_desktop_sessions - 1))

        confirmation = ask_confirmation()

        if not confirmation:
            sys.exit(0)
