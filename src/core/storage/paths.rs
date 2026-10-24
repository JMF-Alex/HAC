use crate::core::constants::APP_NAME;
use std::env;
use std::path::PathBuf;

pub fn data_dir() -> PathBuf {
    if let Some(dir) = env::var_os("HAC_CONFIG_DIR").filter(|d| !d.is_empty()) {
        return PathBuf::from(dir);
    }
    let base = env::var_os("APPDATA")
        .map(PathBuf::from)
        .or_else(|| env::var_os("HOME").map(|h| PathBuf::from(h).join(".config")))
        .unwrap_or_default();
    base.join(APP_NAME)
}

pub fn config_path() -> PathBuf {
    data_dir().join("config.json")
}

pub fn legacy_config_path() -> Option<PathBuf> {
    env::var_os("USERPROFILE").or_else(|| env::var_os("HOME")).map(|h| PathBuf::from(h).join("hac_config.json"))
}
