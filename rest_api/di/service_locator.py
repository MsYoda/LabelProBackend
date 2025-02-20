class ServiceLocator:
    _services = {}

    @classmethod
    def register(cls, service_type, service):
        cls._services[service_type] = service

    @classmethod
    def get(cls, service_type):
        return cls._services.get(service_type)
