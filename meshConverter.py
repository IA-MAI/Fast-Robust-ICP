import vtk
import sys
import os

def convert_ply_to_ascii(input_file, generate_faces=False):
    print("===============   convert_ply_to_ascii  ==================")
    print("input_file : ", input_file)

    # Read the binary PLY file
    reader = vtk.vtkPLYReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    # Get the output
    polydata = reader.GetOutput()

    # Optionally generate faces
    if generate_faces:
        polydata = generate_faces_from_vertices(polydata)

    # Create a writer for ASCII PLY format
    ascii_writer = vtk.vtkPLYWriter()
    ascii_writer.SetFileName(os.path.splitext(input_file)[0] + "_ascii.ply")
    ascii_writer.SetInputData(polydata)
    ascii_writer.SetFileTypeToASCII()
    ascii_writer.Write()
    print(f"Converted {input_file} to ASCII format.")

def convert_ply_to_binary(input_file, generate_faces=False):
    print("===============   convert_ply_to_binary  ==================")
    print("input_file : ", input_file)
    # Read the ASCII PLY file
    reader = vtk.vtkPLYReader()
    reader.SetFileName(input_file)
    reader.Update()
    
    # Get the output
    polydata = reader.GetOutput()

    # Optionally generate faces
    if generate_faces:
        polydata = generate_faces_from_vertices(polydata)

    # Create a writer for binary PLY format
    binary_writer = vtk.vtkPLYWriter()
    binary_writer.SetFileName(os.path.splitext(input_file)[0] + "_bin.ply")
    binary_writer.SetInputData(polydata)
    binary_writer.SetFileTypeToBinary()
    binary_writer.Write()
    print(f"Converted {input_file} to binary format.")

def generate_faces_from_vertices(polydata):
    print("Generating faces from vertices using Surface Reconstruction...")
    
    # Perform surface reconstruction
    surf = vtk.vtkSurfaceReconstructionFilter()
    surf.SetInputData(polydata)
    surf.Update()

    # Convert to polydata
    contour_filter = vtk.vtkContourFilter()
    contour_filter.SetInputConnection(surf.GetOutputPort())
    contour_filter.SetValue(0, 0.0)
    contour_filter.Update()

    # Smooth the surface
    smoother = vtk.vtkSmoothPolyDataFilter()
    smoother.SetInputConnection(contour_filter.GetOutputPort())
    smoother.SetNumberOfIterations(50)
    smoother.SetRelaxationFactor(0.1)
    smoother.FeatureEdgeSmoothingOff()
    smoother.BoundarySmoothingOn()
    smoother.Update()
    
    return smoother.GetOutput()


if __name__ == "__main__":
    print("====================================================")
    print("Point Cloud Converter: PLY to ASCII/Binary\n")
    print("====================================================")
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <convert_to> [generate_faces]")
        print("convert_to: '1:ascii' or '2:binary'")
        print("generate_faces: 'yes' to generate faces (optional)")
        sys.exit(1)

    input_file = sys.argv[1]
    convert_to = sys.argv[2]
    generate_faces = len(sys.argv) > 3 and (sys.argv[3].lower() == "yes" or sys.argv[3].lower() == "1")

    if not os.path.isfile(input_file):
        print(f"Error: {input_file} does not exist.")
        sys.exit(1)

    if convert_to == "ascii" or convert_to == "1":
        convert_ply_to_ascii(input_file, generate_faces)
    elif convert_to == "binary" or convert_to == "2":
        convert_ply_to_binary(input_file, generate_faces)
    else:
        print("Error: Invalid conversion type. Use 'ascii' or 'binary'.")
        sys.exit(1)