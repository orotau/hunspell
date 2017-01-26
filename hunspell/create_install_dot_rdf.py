from yattag import Doc, indent

doc, tag, text, line = Doc().ttl()

doc.asis('<?xml version="1.0"?>')
with tag('RDF',
('xmlns', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
('xmlns:em', 'http://www.mozilla.org/2004/em-rdf#')
):
    with tag('Description', 
    ('about', 'urn:mozilla:install-manifest')
    ):
        line('em:id', 'mi-NZ@dictionaries.addons.mozilla.org')
        line('em:version', 1.0)
        line('em:type', 64)
        line('em:unpack', 'true')
        line('em:name', 'takikupu')

        # Firefox     
        doc.asis('<!-- Firefox -->')
        with tag('em:targetApplication'):
            with tag('Description'):
                line('em:id', '{ec8030f7-c20a-464f-9b0e-13a3a9e97384}')
                line('em:minVersion', '18.0a1')
                line('em:maxVersion', '99')
print(indent(doc.getvalue()))
'''


    <!-- Thunderbird -->
    <em:targetApplication>
      <Description>
        <em:id>{3550f703-e582-4d05-9a08-453d09bdfdc6}</em:id>
        <em:minVersion>18.0a1</em:minVersion>
        <em:maxVersion>22.0</em:maxVersion>
      </Description>
    </em:targetApplication>

    <!-- SeaMonkey -->
    <em:targetApplication>
      <Description>
        <em:id>{92650c4d-4b8e-4d2a-b7eb-24ecf4f6b63a}</em:id>
        <em:minVersion>2.15a1</em:minVersion>
        <em:maxVersion>2.49</em:maxVersion>
      </Description>
    </em:targetApplication>
  </Description>
</RDF>
'''

