#version 410

//in
layout (location = 0) in vec2 in_position;

//out
out vec2 uv_0;
out vec2 pixel_pos;

uniform vec3 pos;
uniform vec3 scale;

void main(){
    uv_0 = vec2(1.0-in_position)/2;
    gl_Position = vec4((vec3(in_position,0.0)+pos)*scale, 1.0);//vector4 for vertex pos
    pixel_pos = vec2(gl_Position);
}