#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use hac::app;
use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            app.manage(app::Controller::new(app.handle().clone()));
            app::start_background(app.handle().clone());
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            app::commands::get_state,
            app::commands::toggle,
            app::commands::select_profile,
            app::commands::add_profile,
            app::commands::duplicate_profile,
            app::commands::rename_profile,
            app::commands::delete_profile,
            app::commands::update_profile,
            app::commands::update_settings,
            app::commands::capture_hotkey,
            app::commands::set_dialog_open,
        ])
        .build(tauri::generate_context!())
        .expect("error while building tauri application")
        .run(|app, event| {
            // releases a held key and flushes the config before the process ends
            if let tauri::RunEvent::Exit = event {
                app.state::<app::Controller>().shutdown();
            }
        });
}
