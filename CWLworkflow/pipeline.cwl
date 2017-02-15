cwlVersion: cwl:v1.0
class: Workflow
inputs:
  directory_in:
    type: Directory

outputs:
  output_json:
    type: File
    outputSource: age/json_out
  gender_out:
    type: File
    outputSource: gender/json_out
  cropped_out:
    type: Directory
    outputSource: face-crop/cropped_out
  detect_json:
    type: File
    outputSource: detect/json_out

steps:
  list_dir:
    run: tools/filestojson.cwl
    in:
      input_files: directory_in
    out:
      - json_out
        
  detect:
    run: tools/yolo.cwl
    in:
      input_json: list_dir/json_out
      input_directory: directory_in
    out: 
      - json_out

  crop:
    run: tools/crop.cwl
    in:
      json_input_file: detect/json_out
      input_directory: directory_in
      probability:
        default: 0.1
    out:
      - json_out
      - cropped_out

  color:
    run: tools/color.cwl
    in:
      json_input: crop/json_out
      input_directory: crop/cropped_out
    out:
      - json_out

  model:
    run: tools/model.cwl
    in:
      json_input: color/json_out
      input_directory: crop/cropped_out
    out:
      - json_out

  face:
    run: tools/face.cwl
    in:
      json_input: model/json_out
      input_directory: crop/cropped_out
    out:
      - json_out

  face-crop:
    run: tools/crop.cwl
    in:
      json_input_file: face/json_out
      input_directory: crop/cropped_out
      probability:
        default: 0.1
      specialised:
        default: true
    out:
      - json_out
      - cropped_out

  gender:
    run: tools/face-gender.cwl
    in:
      json_input: face-crop/json_out
      input_directory: face-crop/cropped_out
    out:
      - json_out


  age:
    run: tools/face-age.cwl
    in:
      json_input: gender/json_out
      input_directory: face-crop/cropped_out
    out:
      - json_out

