import yaml
from cyclonedx.factory.license import LicenseChoiceFactory, LicenseFactory
from cyclonedx.model import OrganizationalEntity, XsUri
from cyclonedx.model.bom import Bom
from cyclonedx.model.component import Component, ComponentType
from cyclonedx.output.json import JsonV1Dot4
from cyclonedx.output.xml import XmlV1Dot4
from packageurl import PackageURL

class YamlConverter:

    def __init__(self) -> None:
        self.lc_factory = LicenseChoiceFactory(license_factory=LicenseFactory())

    def parse(self, path) -> dict:
        with open(path, 'r') as file:
            data = yaml.safe_load(file)
        return data

    def convert(self, path, output):
        json = self.parse(path)
        print(f"{json}")
        bom = Bom()
        bom.metadata.component = rootComponent = Component(
            name=json['name'],
            type=self._getComponentTypeByString(json['type']),
            licenses=[self.lc_factory.make_from_string(json['licence'])],
            bom_ref=json['name']+'@'+json['version'],
            group=json['namespace'],
            version=json['version']
        )

        for component in json['components']:
            supplier_urls = []
            for supplier_url in component['supplier']['urls']:
                supplier_urls.append(XsUri(supplier_url))

            component_tmp = Component(
                type=self._getComponentTypeByString(component['type']),
                name=component['name'],
                group=component['namespace'],
                version=component['version'],
                licenses=[self.lc_factory.make_from_string(component['licence'])],
                supplier=OrganizationalEntity(
                    name=component['supplier']['name'],
                    urls=supplier_urls
                ),
                bom_ref=component['name']+'@'+component['version'],
                purl=PackageURL(component['type'], component['namespace'], component['name'], component['version'])
            )
            bom.components.add(component_tmp)
            bom.register_dependency(rootComponent, [component_tmp])

        XmlV1Dot4(bom).output_to_file(output)
        print(f"{XmlV1Dot4(bom).output_as_string()}")
    
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
        