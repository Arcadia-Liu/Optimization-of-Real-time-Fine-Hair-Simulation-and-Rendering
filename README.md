# Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering

## Abstract:
  As technologies like virtual reality and augmented reality are increasingly applied in gaming, entertainment, and simulation, user demands for realism and immersive experiences continue to rise. Real-time physical simulation and rendering based on reality have thus become focal points in computer graphics research. Among the many factors influencing the realism of characters, hair, with its complexity, variability, and uncontrollability, stands out as one of the most crucial and challenging aspects to achieve in real-time. This paper focuses on real-time fine hair simulation and rendering, delving into how to dynamically simulate and render fine hair in real-time. The main contributions of this work include:

  1. Applying an improved order-independent transparency rendering algorithm to current mainstream real-time fine hair solutions.
  2. Addressing the limitations of traditional hair rendering models, which fail to fully capture the physical properties of hair, by designing and developing a new lighting model.
  3. Integrating the improved real-time fine hair solution into the Unreal Engine. Different types of hair models created in Maya were then bridged into the engine for experimental testing.
  4. Results demonstrate that the improved real-time fine hair solution more accurately restores the realistic form and physical behavior of hair, meeting the basic requirements of practical applications.

## Keywords: 
  real-time rendering, lighting model, hair rendering, hair dynamic simulation, computer graphics

## Real-time Computational Solutions for Realistic Hair Systems

### Polygonal Hair Strands

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/2ab9b969-9dcc-4a19-b85d-e24681f837c9)
  
  Generate a Set of Hair Textures Using the Hair-Strand-Designer Tool

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/d8a4e8c2-11e1-426e-ad2f-67fde814bfac)

  Modeling Faceted Hair with Maya Modeling Tools

### Strand-Based Fine Hair Solutions

  The basic geometric form of hair strands is defined by curves, with model data storing the vertex positions, vertex properties, and control parameters for physical motion and position updates. In Autodesk Maya, artists can create a description zone based on the scalp mesh, which serves as a reference coordinate system to record the segments and points of the strands. To store and refine hair as a collection, the roots must be fixed onto the description zone—this forms the basis of creating hair in Xgen. Xgen allows artists to generate a few guide lines, which can then be interpolated to create a large number of hair strands by adjusting the density, mask maps, and modifiers.

  Xgen generates hair by interpolating between guide lines, simplifying the hair model to a set of guide lines and shifting the computational load to the GPU. When the renderer processes Xgen hair objects, the GPU needs to generate a large number of hair descriptions from a few guide lines and then compute the physical and lighting information for the strands, ultimately rendering them on the screen. Simplifying the modeling process of hundreds of thousands of hair strands is essential for modeling tools, necessitating GPU reliance. However, for real-time game engines, rendering hair models using guide line interpolation imposes a substantial burden on the GPU, making this method impractical.

  Thus, TressFX hair requires representing the actual number of curves, transmitting the hair strand information as model data. The complete workflow necessitates exporting Xgen hair from Maya to TressFX format, including tfxbone skeleton files, tfx hair files, and tfxskin collision skinned mesh files. Xgen provides a "Guides to Curves" tool to convert guide lines into spline curves. According to the TressFX official manual, the character model should be exported as a mesh suitable for SDF (Signed Distance Field) collision detection.

  In 2017, AMD's OpenGPU introduced an export plugin for TressFX hair systems, enabling the export of Xgen hair to a usable format. However, post-2018 versions of Maya saw changes in the Python API, necessitating adjustments to the plugin to accommodate changes in the Pymel system. Additionally, the original export plugin required three separate operations to export tfxbone skeleton files, tfx hair files, and tfxskin collision skinned mesh files. The tfx hair files and tfxskin collision skinned mesh files must be placed in the same directory to bind the hair root nodes to the scalp skin, confirming the distribution of hair clusters. This research consolidates all data into a JSON file using Python and JSON, which is then parsed into tfx hair files and tfxskin collision skinned mesh files upon import into Unreal Engine, where the same binding operations are performed.

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/045da08a-7109-4b5e-8f53-6c32354a82c2)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/0322a6f4-5b29-4fda-aefa-372622df6cf6)

## Research and Improvement of Semi-Transparent Rendering Algorithms for Fine Hair

### Order-Dependent Semi-Transparent Rendering Algorithm for Fine Hair

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/320c2b85-975c-4fb0-a3c9-792c04a2c4fa)

  Alpha Blending Effect in Unreal Engine

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/449b5e41-0149-4bfc-acb6-bf6256600d45)

  Alpha Test Effect in Unreal Engine

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/3ffe92bf-241d-4d90-abca-ae47c3acf896)

### Order-Independent Semi-Transparent Rendering Algorithm for Fine Hair

  The fine hair model is inherently complex, often featuring multiple layers of fragments at the same pixel location. These fragments, all belonging to the hair model, exhibit a high degree of self-interaction. Consequently, order-dependent semi-transparent rendering struggles to achieve desirable results. Traditional solutions require manual differentiation between solid and semi-transparent parts, a method that proves challenging to implement on intricate hair models. In 2007, Meshkin introduced the order-independent semi-transparent rendering algorithm in his GDC report, "Sort-Independent Alpha Blending."

  This algorithm completely discards all computations involving fragment order, employing commutative accumulation operations over 𝑛 fragments. Therefore, there is no need to sort semi-transparent fragments, making it an order-independent rendering algorithm. However, this approach simplifies and omits a significant amount of information, resulting in substantial discrepancies between rendered and real-world outcomes. It may achieve closer results only when Ai is small and Ci colors are similar.

  Similar to traditional methods, order-independent semi-transparent rendering algorithms are based on a concept of color blending. Color information stored at the fragment's position is blended using specific computation methods, and the resulting blend is then outputted to the pixel location on the screen. Thus, the screen display should reflect the result of multiple color blending outputs. However, in the original order-independent alpha blending algorithm, the final color may exceed the range occupied by all fragment colors.

  To optimize the traditional order-independent semi-transparent rendering algorithm, a weighted averaging method is employed. Additional weights are introduced to the original accumulation terms, softening the process of fragment accumulation through averaging.

  Weighted Blended Order-Independent Transparency

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/08f07d7f-af8b-45d4-a410-97ee18e42647)

  Moment Based Order-Independent Transparency

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/d35569d1-250d-41fd-88ea-9036206752d5)


## Research and Improvement of Fine Hair Lighting Models

### Anisotropic Hair-based Kajiya-Kay Lighting Model

  Blinn-Phong Model
  
  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/2152780d-6013-45cc-9a4c-b960e42e993f)

  Kajiya-Kay Model

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/38aeb54a-be98-4b83-b3cc-a303c04752c7)

  Marschner Model

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/3aafabd1-7616-4560-aa54-e08714537f14)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/949fd7f3-2810-468c-9b91-d64b6ef12325)

### Practical Design of Enhanced Fine Hair Systems in Virtual Reality Digital MetaHumans

  Procedurally Generated Head Models Based on Real Human Facial Photographs
  
  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/43cd7ed5-e539-4183-8579-249281aed51e)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/a43994b4-8f66-4092-a099-299d993328c5)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/c137d131-6abe-4dec-8d7b-c5847b2c194f)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/547b8f8d-48c6-41f0-bd1a-697f4ac08d32)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/df8a6312-2c6a-4243-a4e5-341fae1f61ab)

### Guide-Based Fine Hair System for Virtual Digital Humans

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/471066b1-2949-482d-b852-e940b70ed831)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/6766214c-720d-4eec-85a4-8f5958e4a594)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/3721d21d-b36c-4ac9-af25-1f1d9c02081e)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/09a2d534-e30b-4f69-a5e9-5fad62599863)

  ![image](https://github.com/Arcadia-Liu/Optimization-of-Real-time-Fine-Hair-Simulation-and-Rendering/assets/126369162/37784e1f-fdb5-41cc-88b4-6012b38f0aa8)


















  



