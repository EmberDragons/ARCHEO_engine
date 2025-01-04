#version 410
#define MAX_SIZE 24

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
out vec4 shadowCoord[MAX_SIZE];

//matrices
uniform mat4 m_proj;
uniform mat4 m_view;

uniform mat4 m_view_l[MAX_SIZE];
uniform int number_mat[4];
uniform int number_lights;
uniform mat4 m_proj_l[4];
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

    //depth textures
    int nb = 0;
    for (int y = 0; y<number_lights; y++){
        for (int i = 0; i<number_mat[y]; i++){
            mat4 shadowMVP = m_proj_l[y]*m_view_l[i+y*6]*m_model;
            shadowCoord[i+nb] = m_bias*shadowMVP*vec4(in_position,1.0);
            shadowCoord[i+nb].z-=0.005;
        }
        nb+=number_mat[y];
    }
    
    //lighting
    v_pos = vec3(m_model*vec4(in_position, 1.0)); 
    v_normals = normalize(mat3(transpose(inverse(m_model)))*normalize(in_normales)); //vector4 for the normal of the vertices
    rd_light_diffraction = random(vec2(in_texcoord.x*22+41, in_texcoord.y*43+63)); //pseudo-random number generator
}