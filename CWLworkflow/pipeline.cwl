cwlVersion: cwl:v1.0
class: Workflow
inputs:
  directory_in:
    type: Directory

outputs:
  output_json:
    type: File
    outputSource: detect/workflow_out

steps:
  list_dir:
    run: tools/filestojson.cwl
    in:
      input_files:
        source: directory_in
      workflow_out:
        default: files.json
    out:
      - files_out
        
  detect:
    run: tools/ssd-coco.cwl
    in:
      input_json:
        source: list_dir/files_out
      workflow_out:
        default: detect.json
      input_directory:
        source: directory_in
    out: 
      - workflow_out

