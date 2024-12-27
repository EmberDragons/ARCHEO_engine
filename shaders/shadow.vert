#version 410

layout(location = 2) in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_view_l;
uniform mat4 m_model;

void main(){
    mat4 mvp = m_proj*m_view_l*m_model;
    gl_Position = mvp * vec4(in_position,1.0);
}