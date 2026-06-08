from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from elecciones.models import Candidacy


class Command(BaseCommand):
    help = 'Carga datos de ejemplo para Votasena'

    def handle(self, *args, **options):
        sample_students = [
            {'username': 'Rodrigo Castaño', 'password': 'Aprendiz2026!', 'ficha': '3229879'},
            {'username': 'Daniel Barbosa', 'password': 'Aprendiz2026!', 'ficha': '3229879'},
            {'username': 'Valeria Alvarez', 'password': 'Aprendiz2026!', 'ficha': '4456123'},
        ]

        sample_candidates = [
            {
                'name': 'Ana Gómez',
                'role': Candidacy.ROLE_REPRESENTANTE,
                'ficha': None,
                'description': 'Tengo 21 años, soy alegre, me encanta ayudar a los demás y leer mucho.',
                'proposals': 'Mejorar la infraestructura del centro\nImplementar programas de becas\nReforzar espacios de integración estudiantil',
                'profile_image': 'elecciones/img/candidate-1.svg'
            },
            {
                'name': 'Carlos Herrera',
                'role': Candidacy.ROLE_REPRESENTANTE,
                'ficha': None,
                'description': 'Soy aprendiz de sistemas y me apasiona trabajar en equipo y escuchar a todos.',
                'proposals': 'Crear espacios de mentoría con aprendices mayores\nGestionar mejores horarios para actividades extraacadémicas\nPromover inclusión y diversidad en todas las aulas',
                'profile_image': 'elecciones/img/candidate-2.svg'
            },
            {
                'name': 'María Rodríguez',
                'role': Candidacy.ROLE_REPRESENTANTE,
                'ficha': None,
                'description': 'Soy responsable, me gusta organizar y sueño con una comunidad más unida.',
                'proposals': 'Fortalecer la relación entre aprendices y administración\nImplementar sugerencias mensuales de los aprendices\nBrindar apoyo en trámites académicos',
                'profile_image': 'elecciones/img/candidate-3.svg'
            },
            {
                'name': 'Laura Pérez',
                'role': Candidacy.ROLE_VOCERO,
                'ficha': '3229879',
                'description': 'Tengo 22 años, me gusta escuchar a mis compañeros y encontrar soluciones juntos.',
                'proposals': 'Organizar actividades de integración para nuestra ficha\nGestionar más espacios de estudio entre clases\nMejorar la comunicación interna del grupo',
                'profile_image': 'elecciones/img/candidate-4.svg'
            },
            {
                'name': 'Andrés Torres',
                'role': Candidacy.ROLE_SUBVOCERO,
                'ficha': '3229879',
                'description': 'Soy tranquilo, organizado y siempre dispuesto a apoyar en lo que haga falta.',
                'proposals': 'Apoyo logístico en eventos de la ficha\nPromoción de compañerismo entre los aprendices\nGestionar recursos para el grupo',
                'profile_image': 'elecciones/img/candidate-5.svg'
            },
            {
                'name': 'Pedro Perez',
                'role': Candidacy.ROLE_VOCERO,
                'ficha': '3229879',
                'description': 'Me gusta aprender, colaborar y mantener al grupo unido en momentos importantes.',
                'proposals': 'Crear un grupo de estudio colaborativo permanente\nOrganizar actividades recreativas mensuales\nMejorar el ambiente de trabajo y las reuniones',
                'profile_image': 'elecciones/img/candidate-1.svg'
            },
            {
                'name': 'Carolina Campo',
                'role': Candidacy.ROLE_SUBVOCERO,
                'ficha': '3229879',
                'description': 'Soy creativa, comunicativa y siempre busco que el equipo avance con buena onda.',
                'proposals': 'Facilitar la comunicación grupal de la ficha\nOrganizar reuniones efectivas y bien planificadas\nApoyar proyectos colectivos con buena coordinación',
                'profile_image': 'elecciones/img/candidate-2.svg'
            },
            {
                'name': 'Maria Valencia',
                'role': Candidacy.ROLE_VOCERO,
                'ficha': '3229879',
                'description': 'Soy proactiva, empática y me interesa que todos se sientan escuchados.',
                'proposals': 'Impulsar el liderazgo compartido entre compañeros\nGestionar problemas académicos con claridad\nFomentar la responsabilidad y el respeto mutuo',
                'profile_image': 'elecciones/img/candidate-3.svg'
            },
            {
                'name': 'Camilo Rodríguez',
                'role': Candidacy.ROLE_SUBVOCERO,
                'ficha': '3229879',
                'description': 'Me gusta apoyar a mis amigos y ser el puente entre el grupo y los líderes.',
                'proposals': 'Documentar decisiones del grupo para mayor transparencia\nApoyar las organizaciones internas con constancia\nFacilitar el acceso a recursos y materiales',
                'profile_image': 'elecciones/img/candidate-4.svg'
            },
            {
                'name': 'Daniela Suárez',
                'role': Candidacy.ROLE_VOCERO,
                'ficha': '4456123',
                'description': 'Soy entusiasta, me encanta trabajar con personas y escuchar nuevas ideas.',
                'proposals': 'Crear un canal de comunicación eficiente para la ficha\nOrganizar eventos sociales y académicos\nMejorar el ambiente de convivencia entre compañeros',
                'profile_image': 'elecciones/img/candidate-5.svg'
            },
            {
                'name': 'Santiago Mejía',
                'role': Candidacy.ROLE_SUBVOCERO,
                'ficha': '4456123',
                'description': 'Soy ordenado, perseverante y dispuesto a colaborar con todos los compañeros.',
                'proposals': 'Brindar apoyo en actividades grupales y dinámicas\nGestionar recursos educativos con responsabilidad\nPromover la participación activa de la ficha',
                'profile_image': 'elecciones/img/candidate-1.svg'
            },
            {
                'name': 'Rodrigo Silva',
                'role': Candidacy.ROLE_VOCERO,
                'ficha': '4456123',
                'description': 'Soy responsable, me esfuerzo y quiero ser voz de los aprendices en mi ficha.',
                'proposals': 'Fortalecer los lazos de compañerismo en la ficha\nGestionar espacios de encuentro regulares\nIncentivar proyectos colaborativos entre todos',
                'profile_image': 'elecciones/img/candidate-2.svg'
            },
            {
                'name': 'Leonardo Lozano',
                'role': Candidacy.ROLE_SUBVOCERO,
                'ficha': '4456123',
                'description': 'Me gusta ayudar, escuchar y apoyar a mi grupo en todo lo que necesite.',
                'proposals': 'Facilitar la comunicación efectiva interna\nOrganizar eventos académicos con sentido práctico\nMejorar el seguimiento de iniciativas del grupo',
                'profile_image': 'elecciones/img/candidate-3.svg'
            },
            {
                'name': 'Julio Bernal',
                'role': Candidacy.ROLE_VOCERO,
                'ficha': '4456123',
                'description': 'Soy amigable, creativo y siempre busco que mi grupo se sienta bien.',
                'proposals': 'Crear espacios de diálogo abierto entre compañeros\nGestionar necesidades del grupo con empatía\nPromover el desarrollo personal y académico',
                'profile_image': 'elecciones/img/candidate-4.svg'
            },
            {
                'name': 'Juan Martínez',
                'role': Candidacy.ROLE_SUBVOCERO,
                'ficha': '4456123',
                'description': 'Soy comprometido y me importa que los compañeros tengan apoyo.',
                'proposals': 'Documentar procesos y mantener claridad administrativa\nBrindar apoyo administrativo grupal\nFacilitar la comunicación entre los miembros',
                'profile_image': 'elecciones/img/candidate-5.svg'
            },
        ]

        for student in sample_students:
            username = student['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'El usuario {username} ya existe.'))
                continue
            user = User.objects.create_user(username=username, password=student['password'])
            user.profile.ficha = student['ficha']
            user.profile.save()
            user.is_staff = False
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Usuario de ejemplo creado: {username}'))

        for candidate_data in sample_candidates:
            candidate, created = Candidacy.objects.get_or_create(
                name=candidate_data['name'],
                role=candidate_data['role'],
                ficha=candidate_data['ficha'],
                defaults={
                    'description': candidate_data['description'],
                    'proposals': candidate_data.get('proposals', ''),
                    'profile_image': candidate_data.get('profile_image', ''),
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Candidato creado: {candidate.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Candidato ya existente: {candidate.name}'))

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo cargados correctamente.'))
