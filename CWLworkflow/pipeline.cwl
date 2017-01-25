cwlVersion: cwl:v1.0
class: Workflow
inputs:
  directory_in:
    type: Directory

outputs:
  output_json:
    type: File
    outputSource: crop/json_out
  cropped_out:
    type: Directory
    outputSource: crop/cropped_out

steps:
  list_dir:
    run: tools/filestojson.cwl
    in:
      input_files:
        source: directory_in
      workflow_out:
        default: files.json
    out:
      - json_out
        
  detect:
    run: tools/ssd-coco.cwl
    in:
      input_json:
        source: list_dir/json_out
      workflow_out:
        default: detect.json
      input_directory:
        source: directory_in
    out: 
      - json_out

  crop:
    run: tools/crop.cwl
    in:
      json_input_file:
        source: detect/json_out
      workflow_out:
        default: cropped.json
      input_directory:
        source: directory_in
      probability:
        default: 0.2
    out:
      - json_out
      - cropped_out
