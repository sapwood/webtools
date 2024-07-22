from flask import Flask, render_template, request, jsonify
import ipaddress

app = Flask(__name__)

def is_valid_number(number, base):
    try:
        int(number, base)
        return True
    except ValueError:
        return False

def convert_number(number, from_base, to_base):
    if from_base == 10:
        decimal_number = int(number)
    else:
        decimal_number = int(number, from_base)
    
    if to_base == 10:
        return str(decimal_number)
    elif to_base == 2:
        return bin(decimal_number)[2:]
    elif to_base == 8:
        return oct(decimal_number)[2:]
    elif to_base == 16:
        return hex(decimal_number)[2:]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/converter')
def converter():
    return render_template('number-converter.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    number = data['number']
    from_base = int(data['from_base'])
    to_base = int(data['to_base'])
    
    if not is_valid_number(number, from_base):
        return jsonify(error="Invalid number for the specified base"), 400

    result = convert_number(number, from_base, to_base)
    return jsonify(result=result)

# @app.route('/subnet_calculator')
# def subnet_calculator():
#     return render_template('subnet_calculator.html')

# @app.route('/calculate_subnets', methods=['POST'])
# def calculate_subnets():
#     data = request.json
#     network_address = data['network_address']
#     slash_notation = int(data['slash_notation'])
#     subnets = data['subnets']

#     try:
#         network = ipaddress.ip_network(f"{network_address}/{slash_notation}", strict=False)
#     except ValueError:
#         return jsonify(error="Invalid network address or slash notation"), 400

#     calculated_subnets = []
#     for subnet in subnets:
#         subnet_size = int(subnet['size'])
#         subnet_prefix = 32 - subnet_size.bit_length() + 1
#         subnet_list = list(network.subnets(new_prefix=subnet_prefix))
#         if len(subnet_list) == 0:
#             return jsonify(error=f"Cannot create subnet with size {subnet_size}"), 400
#         calculated_subnets.append(str(subnet_list[0]))
#         network = list(network.address_exclude(subnet_list[0]))[0]

#     return jsonify(subnets=calculated_subnets)

if __name__ == '__main__':
    app.run()
