#version 410

//in
layout (location = 1) in vec2 in_position;

//out
out vec2 pixel_pos;


void main(){
    gl_Position = vec4(in_position, 0.0, 1.0);//vector4 for vertex pos
    pixel_pos = vec2(gl_Position);
}