#version 410

//in
layout (location = 0) in vec2 in_texcoord;
layout (location = 1) in vec3 in_position;
layout (location = 2) in vec3 in_normales;

//out
out vec2 uv_0;
out vec3 v_pos;
out vec3 v_normals;
out float rd_light_diffraction;
out vec2 pixel_pos;
out vec4 shadowCoord;

//matrices
uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_view_l;
uniform mat4 m_model;

uniform mat4 m_bias = mat4(
    0.5,0.0,0.0,0.0,
    0.0,0.5,0.0,0.0,
    0.0,0.0,0.5,0.0,
    0.5,0.5,0.5,1.0
);

float random(vec2 st){
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main(){
    uv_0 = vec2(1.0-in_texcoord);
    gl_Position = m_proj*m_view*m_model*vec4(in_position, 1.0);//vector4 for vertex pos
    pixel_pos = vec2(gl_Position);

    //depth tex
    mat4 shadowMVP = m_proj*m_view_l*m_model;
    shadowCoord = m_bias*shadowMVP*vec4(in_position,1.0);
    shadowCoord.z-=0.0005;
    
    //lighting
    v_pos = vec3(m_model*vec4(in_position, 1.0)); 
    v_normals = normalize(mat3(transpose(inverse(m_model)))*normalize(in_normales)); //vector4 for the normal of the vertices
    rd_light_diffraction = random(vec2(in_texcoord.x*22+41, in_texcoord.y*43+63)); //pseudo-random number generator
}