#version 410

//in
layout (location = 0) in vec2 in_pos;

void main(){
    gl_Position = vec4(in_pos,0.0,1.0);//vector4 for vertex pos
}