cwlVersion: cwl:v1.0
class: Workflow
inputs:
  directory_in:
    type: Directory
  filename:
    type: string
  user:
    type: string
  password:
    type: string
  webdav_url:
    type: string

outputs:
  url:
    type: string
    outputSource: upload/url
  #output_json:
  #  type: File
  #  outputSource: age/json_out
  #gender_out:
  #  type: File
  #  outputSource: gender/json_out
  #cropped_out:
  #  type: Directory
  #  outputSource: face-crop/cropped_out
  #detect_json:
  #  type: File
  #  outputSource: detect/json_out

requirements:
   MultipleInputFeatureRequirement: {}

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

  images_json:
    run: tools/images_json.cwl
    in:
      json_input: age/json_out
    out:
      - json_out

  upload:
    run: tools/upload-webdav.cwl
    in:
      json_input: images_json/json_out
      directories:
        source:
          - crop/cropped_out
          - face-crop/cropped_out
      filename: filename
      user: user
      password: password
      webdav_url: webdav_url
    out:
      - url
  
