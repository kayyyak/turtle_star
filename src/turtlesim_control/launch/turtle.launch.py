from launch import LaunchDescription, LaunchContext
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, OpaqueFunction
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os
import yaml

def modify_new_path_control(full_path:str, new_path:str, namespace:str) -> None:
    with open(full_path, 'r') as file:
        data = yaml.load(file, yaml.SafeLoader)
    new_data = {namespace: data}

    with open(new_path, 'w') as file:
        yaml.dump(new_data, file)
    
def render_namespace(context:LaunchContext, launch_description:LaunchDescription, via_name:LaunchConfiguration, turtle_name:LaunchConfiguration) -> None:
    via_name_str = context.perform_substitution(via_name)
    path = get_package_share_directory('turtlesim_control')
    via_path = os.path.join(path, 'via_point', via_name_str)
    
    turtle_name_str = context.perform_substitution(turtle_name)
    config_path = os.path.join(path, 'config', 'controller_01.yaml')
    new_path = os.path.join(path, 'config', 'controller_01'+turtle_name_str+'.yaml')
    modify_new_path_control(config_path, new_path, turtle_name_str)

    controller = Node(package = 'turtlesim_control', 
                      executable = 'controller.py', 
                      namespace = turtle_name, 
                      parameters = [new_path])
    
    scheduler = Node(package = 'turtlesim_control', 
                executable = 'scheduler.py', 
                namespace = turtle_name, 
                arguments = ['-f', via_path])

    launch_description.add_action(controller)
    launch_description.add_action(scheduler)

def generate_launch_description():
    x_launch_arg = DeclareLaunchArgument('x', default_value = '2.0')
    y_launch_arg = DeclareLaunchArgument('y', default_value = '2.0')
    namespace_launch_arg = DeclareLaunchArgument('tao_name')
    file_via = DeclareLaunchArgument('file') # default_value = '/home/kaymarrr/fra501_ws/src/turtlesim_control/via_point/via_point_01.yaml'
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    turtle_name = LaunchConfiguration('tao_name')
    via_f = LaunchConfiguration('file')

    cmd = LaunchConfiguration('cmd', default = ['ros2 service call /spawn turtlesim/srv/Spawn "{x: ',x,
    ', y: ',y,
    ', theta: 0.0'
    ', name: ',turtle_name,
    '}"'])
    spawn_turtle = ExecuteProcess(cmd = [[cmd]], shell = True)
    
    kill_turtle = ExecuteProcess(cmd = [['ros2 service call /kill turtlesim/srv/Kill "{name: \'turtle1\'}"']],
        shell = True)
    
    turtlesim = Node(package = 'turtlesim', 
                     executable = 'turtlesim_node')


    launch_description = LaunchDescription()

    opaque_function = OpaqueFunction(function = render_namespace, args = [launch_description, via_f, turtle_name])

    launch_description.add_action(x_launch_arg)
    launch_description.add_action(y_launch_arg)
    launch_description.add_action(namespace_launch_arg)
    launch_description.add_action(file_via)
    launch_description.add_action(turtlesim)
    launch_description.add_action(kill_turtle)
    launch_description.add_action(spawn_turtle)
    launch_description.add_action(opaque_function)
    
    #ros2 launch turtlesim_control turtle.launch.py

    #ros2 launch turtlesim_control turtle.launch.py x:=5.5 y:=5.5 tao_name:=' ' file:=' '

    return launch_description