import os
import unreal

def export_data_tables():
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    content_path = "/Game/"
    asset_data_list = asset_registry.get_assets_by_path(content_path, recursive=True)

    data_table_count = 0
    exported_count = 0

    print(f"Exporting Data Table:")

    for asset_data in asset_data_list:
        asset_class_path = asset_data.asset_class_path

        if asset_class_path == "/Script/Engine.DataTable":
            data_table_count += 1
            
    text_label = "Exporting Data Tables"
    with unreal.ScopedSlowTask(data_table_count, text_label) as slow_task:
        slow_task.make_dialog(True)

        addon_directory = os.path.join(os.path.dirname(__file__), "..")  # Adjust this path accordingly
        export_subdir = os.path.join(addon_directory, "ExportedDataTables")

        for index, asset_data in enumerate(asset_data_list):
            asset_path = asset_data.asset_name
            asset_type = asset_data.asset_class

            if asset_type == "DataTable":
                asset_name = unreal.Paths.get_base_filename(asset_path)
                export_path = os.path.join(export_subdir, f"{asset_name}.csv")
                data_table = unreal.EditorAssetLibrary.load_asset(asset_path)

                if data_table:
                    unreal.DataTableFunctionLibrary.export_to_csv(data_table, export_path)
                    exported_count += 1

                slow_task.enter_progress_frame(1)

                if slow_task.should_cancel():
                    break

    print(f"Exported {exported_count}/{data_table_count} data tables.")


