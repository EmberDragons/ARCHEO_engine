#version 410

layout (location = 0) in vec2 uv_0;
layout (location = 1) in vec3 v_pos;
layout (location = 4) in vec2 pixel_pos;


out vec4 fragColor;

uniform vec3 cam_pos;

uniform sampler2D u_texture_0;

//matrices
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main(){
    vec3 v_cam = normalize(cam_pos-v_pos); //vector3 for the cam vector


    vec3 raw_color = texture(u_texture_0, uv_0).rgb;
    float r = raw_color.r;
    float g = raw_color.g;
    float b = raw_color.b;
    vec3 color = vec3(r,g,b);
    

    fragColor = vec4(color+v_cam*0.00001, 1.0);
}