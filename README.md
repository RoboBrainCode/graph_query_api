graph_query_api
===============

### Graph Structure
1. Nodes have either the label :Concept or :Media. If they have :Media, they will also have a :Image, :Video or :Text label depending on what media type they represent.
2. Edges store the source_url, source_text and keywords (an array of strings) properties. Each edge is labeled by its edge type. For example, an edge representing the spatially_distributed_as relationship will have the :SPATIALLY_DISTRIBUTED_AS label.
3. Nodes store the handle name without the #. eg. {handle: 'shoe'}
4. :Media nodes referred to in the source_text with a #$ will have the word following #$ as the handle name. eg. #$image -> {handle: 'image'}
5. :Media nodes NOT referred to in the source_text will have the file name of the media as the handle name and the full url path of the media as mediapath. eg. 'aaa/bbb/shoe.jpg' -> {handle: 'shoe.jpg', mediapath: 'aaa/bbb/shoe.jpg'}
