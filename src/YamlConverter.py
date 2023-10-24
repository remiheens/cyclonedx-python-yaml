import yaml
from typing import Iterable
from cyclonedx.factory.license import LicenseChoiceFactory, LicenseFactory
from cyclonedx.model import OrganizationalEntity, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output.xml import XmlV1Dot4

class YamlConverter:

    def __init__(self, *, version: int = 1) -> None:
        self.lc_factory = LicenseChoiceFactory(license_factory=LicenseFactory())
        self.bom_version = version

    def parse(self, path) -> dict:
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def convert(self, path, output):
        json = self.parse(path)
        print(f"{json}")
        self._bom = Bom(version=self.bom_version)
        self._bom.metadata.component = rootComponent = self.generate_component(json)
        
        for component in json['components']:
            self.parse_components(self._bom, component)
            self._bom.register_dependency(rootComponent, self._bom.components)

        XmlV1Dot4(self._bom).output_to_file(output)
        print(f"{XmlV1Dot4(self._bom).output_as_string()}")
    
    def extraction_depends(self, obj):
        results = []
        for component in obj.components:
            results.append(dict({"bom_ref": component.bom_ref, "depends_on": self.extraction_depends(component)}))
        return results

    def parse_components(self, root, obj):
        cmp = self.generate_component(obj)
    
        for component in obj['components'] if ('components' in obj) else []:
            self.parse_components(cmp, component)
            self._bom.register_dependency(cmp, cmp.components)
        root.components.add(cmp)
        return root

    def _getComponentTypeByString(self, type) -> ComponentType:
        if type == "application":
            return ComponentType.APPLICATION
        if type == "framework":
            return ComponentType.FRAMEWORK
        if type == "library":
            return ComponentType.LIBRARY
        if type == "container":
            return ComponentType.CONTAINER
        if type == "operating-system":
            return ComponentType.OPERATING_SYSTEM
        if type == "device":
            return ComponentType.DEVICE
        if type == "firmware":
            return ComponentType.FIRMWARE
        if type == "file":
            return ComponentType.FILE
        
    def generate_component(self, obj) -> Component:
        component = Component(
            name=obj['name'],
            type=self._getComponentTypeByString(obj['type']),
            bom_ref=(str(obj['name']+'@'+obj['version']) if 'version' in obj else None),
            namespace=(str(obj['namespace']) if 'namespace' in obj else None)
        )
        
        if ('description' in obj):
            component.description = obj['description']
        if ('version' in obj):
            component.version = obj['version']
        if ('copyright' in obj):
            component.copyright = obj['copyright']
        if ('publisher' in obj):
            component.publisher = obj['publisher']
        if ('group' in obj):
            component.group = obj['group']
        if ('author' in obj):
            component.author = obj['author']
        if ('license' in obj):
            component.licenses = self.generate_licenses(obj['license'])
        if ('supplier' in obj):
            component.supplier = self.generate_supplier(obj['supplier'])

        return component
    
    def generate_licenses(self, license) -> Iterable[LicenseFactory]:
        return [self.lc_factory.make_from_string(license)]

    def generate_supplier(self, obj) -> OrganizationalEntity:
        
        if ('name' in obj):
            supplier = OrganizationalEntity(name=obj['name'])

        supplier_urls = []
        for supplier_url in obj['urls'] if ('urls' in obj) else []:
            supplier_urls.append(XsUri(supplier_url))
        if isinstance(supplier, OrganizationalEntity):
            supplier.urls = supplier_urls 
        else:
            supplier = OrganizationalEntity(urls=supplier_urls)

        return supplier