cwlVersion: cwl:v1.0
class: Workflow
inputs:
  directory_in:
    type: Directory

outputs:
  output_json:
    type: File
    outputSource: model/json_out
  color_json:
    type: File
    outputSource: color/json_out
  cropped_out:
    type: Directory
    outputSource: crop/cropped_out
  detect_json:
    type: File
    outputSource: detect/json_out

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
        default: 0.1
      cropped_folder:
        default: cropped
    out:
      - json_out
      - cropped_out

  color:
    run: tools/color.cwl
    in:
      json_input:
        source: crop/json_out
      workflow_out:
        default: color.json
      input_directory:
        source: crop/cropped_out
    out:
      - json_out

  model:
    run: tools/model.cwl
    in:
      json_input:
        source: color/json_out
      workflow_out:
        default: model.json
      input_directory:
        source: crop/cropped_out
    out:
      - json_out

  face:
    run: tools/face.cwl
    in:
      json_input:
        source: model/json_out
      workflow_out:
        default: face.json
      input_directory:
        source: crop/cropped_out
    out:
      - json_out
