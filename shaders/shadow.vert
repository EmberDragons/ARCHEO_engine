#version 410

layout(location = 2) in vec3 in_position;

uniform mat4 m_proj; //THAT IS PROBLEM 
uniform mat4 m_view_light;
uniform mat4 m_model;

void main(){
    mat4 mvp = m_proj*m_view_light*m_model;
    gl_Position = mvp * vec4(in_position,1.0);
}