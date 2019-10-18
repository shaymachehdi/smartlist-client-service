from flask import request, jsonify, Blueprint, current_app, url_for, make_response
from flask_marshmallow import Marshmallow
from userservice.myservices.device.models  import Device
from userservice import db, bcrypt, login_manager, app
from flask_login import login_user, current_user, logout_user, login_required
from userservice.myservices.decorators import require_appkey, token_required
from userservice.myservices.users.models import Registreduser
import jwt
from datetime import datetime

devices = Blueprint('devices', __name__)
# Init marshmallow
ma = Marshmallow(devices)
# User Schema
class DeviceSchema(ma.Schema):
  class Meta:
    fields = ('idDevice', 'localisation', 'code_device' ,'email', 'install_at', 'levelConfidence_device')

# Init schema
device_schema = DeviceSchema(strict=True)
devices_schema = DeviceSchema(many=True, strict=True)


# Create Device
@devices.route('/deviceAdd', methods=['POST'])
def create_Device():
        localisation = request.json['localisation']
        email = request.json['email']
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        code = date_time+request.json['codeImei']
        code_device = bcrypt.generate_password_hash(code).decode('utf-8')
        new_device = Device( localisation , email ,datetime.utcnow(),code_device)
        db.session.add(new_device)
        db.session.commit()
        #return user_schema.jsonify(new_Device)
        return jsonify ({
            'msg': 'New device successfully created !'
        })

#getallDevice
@devices.route('/device', methods=['GET'])
@require_appkey
def get_devices():
    all_devices =Device.query.all()
    result = devices_schema.dump(all_devices)
    return jsonify(result.data)
# Update Device info
@devices.route('/device/update', methods=['PUT'])
@require_appkey
def update_device():

    code_device = request.json['code_device']
    # Fetch user
    device = Device.query.filter_by (code_device=code_device).first ()
    if not device:
        return jsonify ({ 'msg': 'No device found!',

                          })
    # update fields
    localisation = request.json['localisation']
    levelConfidence = request.json['levelConfidence_device']

    device.localisation = localisation
    device.levelConfidence_device = levelConfidence
    db.session.commit()

    return jsonify ({ 'msg': 'User successfully updated!',
                      'localisation': device.localisation,
                      'email': device.email ,
                      'levelConfidence': device.levelConfidence_device,
                      'install_at': device.install_at })

# Delete Device
@devices.route('/device/delete', methods=['DELETE'])
@require_appkey
def delete_device():
  code_device = request.json['code_device']
  device = Device.query.filter_by (code_device=code_device).first ()

  if not device:
    return jsonify ({ 'msg': 'No device found!' })

  db.session.delete (device)
  db.session.commit ()

  return jsonify ({ 'msg': 'device successfully deleted!' })


# Attach device to user
@devices.route('/device/attach', methods=['PUT'])
@require_appkey
def attachDeviceToUser():
    code_device = request.json['code_device']
    emailUser = request.json['emailUser']
    # Fetch user
    device = Device.query.filter_by (code_device=code_device).first ()
    user= Registreduser.query.filter_by (email=emailUser).first ()
    if not device or not user:
        return jsonify ({ 'msg': 'No user found!',
                          'isAttached': False
                          })
    device.user_id = user.id
    db.session.commit()
    return jsonify ({ 'msg': 'Device successfully attached!',
                      'isAttached': True,
                      'email': device.email,
                      'user_id' : device.user_id
                       })

# detach device from user
@devices.route('/device/detach', methods=['PUT'])
@require_appkey
def detachDeviceFromUser():
    code_device = request.json['code_device']
    emailUser = request.json['emailUser']
    # Fetch user
    device = Device.query.filter_by (code_device=code_device).first ()
    user= Registreduser.query.filter_by (email=emailUser).first ()
    if not device or not user:
        return jsonify ({ 'msg': 'No user found!',
                          'isDetached': False
                          })
    device.user_id = None
    db.session.commit()
    return jsonify ({ 'msg': 'Device successfully detached!',
                      'isDetached': True,
                      'email': device.email,
                      'user_id' :None
                       })


