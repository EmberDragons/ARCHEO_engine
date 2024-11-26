#version 410

//in
layout (location = 0) in vec2 in_texcoord;
layout (location = 1) in vec3 in_position;

//out
out vec2 uv_0;
out vec3 v_pos;
out vec2 pixel_pos;

//matrices
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main(){
    uv_0 = vec2(1.0-in_texcoord);
    gl_Position = m_proj*m_view*m_model*vec4(in_position, 1.0);//vector4 for vertex pos
    pixel_pos = vec2(gl_Position);

    
    //lighting
    v_pos = vec3(m_model*vec4(in_position, 1.0)); 
}