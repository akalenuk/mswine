#!/usr/bin/python2.7
#
# Copyright 2011 Alexandr Kalenuk.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


""" simple Wavefromn .obj import/export

Only the basic functionallity providen. Mostly for vertices and faces only

"""

__authors__ = [
  '"Alexandr Kalenuk" <akalenuk@gmail.com>'
]

def put_vertices_and_faces_to(file_name, vertices, faces):
    to_file = []
    to_file += ['# vertices\n']    
    
    for v in vertices:
        to_file += ['v ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n']

    to_file += ['\n# faces\n']
    for f in faces:
        to_file += ['f ' + str(f[0]) + ' ' + str(f[1]) + ' ' + str(f[2]) + '\n']

    f = open(file_name, 'w')
    f.writelines(to_file)
    f.close()


def get_from(file_name, what = 'v', with_his_type = 1.0):
    something = []
    f = open(file_name, 'r')
    text = f.read()
    lines = text.split('\n')
    for line in lines:
        chunks = [chunk for chunk in line.split(' ') if chunk!='']
        if chunks == []: continue
        if chunks[0] == what:
            something += [[type(with_his_type)(chunk) for chunk in chunks[1:]]]
    f.close()
    return something


def clear(file_name):
    f = open(file_name, 'w')
    f.close()


def append_to(file_name, what, data, note = '\n'):
    to_file = []
    to_file += ['\n# ' + note + '\n']
    
    for piece in data:
        to_file += [what + ' ' + ' '.join([str(x) for x in piece]) + '\n']
    
    f = open(file_name, 'a')
    f.writelines(to_file)
    f.close()


def swap_vertices_in(file_name, new_vertices, new_file_name = ''):
    f = open(file_name, 'r')
    lines = f.read().split('\n')
    f.close()
    
    new_lines = []
    i=0
    for line in lines:
        trimmed = line.lstrip()
        if len(trimmed)>1 and trimmed[:2] == 'v ':
            new_lines+=['v ' + ' '.join([str(x) for x in new_vertices[i]]) + '\n']
            i+=1
        else:
            new_lines+=[line+'\n']

    if new_file_name=='':
        new_file_name = file_name
    f = open(new_file_name, 'w')
    f.writelines(new_lines)
    f.close()

    
def get_vertices_from(file_name):
    return get_from(file_name, 'v', 0.0)


def get_faces_from(file_name):
    return get_from(file_name, 'f', 0)


def square_mesh_to_obj(mesh, file_name):
    mesh_h = len(mesh)
    mesh_w = len(mesh[0])
    
    to_file = []
    to_file += ['# vertices\n']
    
    for mesh_line in mesh:
        for v in mesh_line:
            to_file += ['v ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + '\n']

    to_file += ['# faces\n']
    for i in range(0, mesh_h-1):
        for j in range(0, mesh_w-1):
            ul = 1 + i*mesh_w + j
            ur = 1 + i*mesh_w + j + 1
            bl = 1 + (i+1)*mesh_w + j
            br = 1 + (i+1)*mesh_w + j + 1
            to_file += ['f ' + str(ul) + ' ' + str(ur) + ' ' + str(br) + '\n']
            to_file += ['f ' + str(ul) + ' ' + str(br) + ' ' + str(bl) + '\n']

    f = open(file_name, 'w')
    f.writelines(to_file)
    f.close()


    
if __name__ == '__main__':
    ''' testing and demonstration part '''

    vertices = [[1.3, 2.8, 1.4], [1.3, 8.7, 1.4], [9.6, 8.7, 1.4], [9.6, 2.8, 1.4]]
    faces = [[1, 2, 3], [1, 3, 4]]
   
    clear('test.obj')
    append_to('test.obj', 'v', vertices, 'Vertices')
    append_to('test.obj', 'f', faces, 'Faces')        
    print get_from('test.obj', 'v')[0]
    print get_from('test.obj', 'f', 1)[0]    
    print
    
    put_vertices_and_faces_to('test.obj', vertices, faces)
    
    vertices[0][0] = 0.0
    swap_vertices_in('test.obj', vertices, 'test2.obj')
    print get_vertices_from('test2.obj')[0]
    print get_faces_from('test2.obj')[0]


