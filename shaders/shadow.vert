#version 410

layout(location = 2) in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_view_l;
uniform mat4 m_model;

flat out vec3 fragPositionLightSpace;

void main(){
    fragPositionLightSpace = vec3(m_model * vec4(in_position,1.0));
    gl_Position = m_proj * m_view_l * vec4(fragPositionLightSpace,1.0);
}