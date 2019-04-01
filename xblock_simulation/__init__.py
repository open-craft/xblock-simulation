# -*- coding: utf-8 -*-
"""
Simulation XBlock
"""
import json
import logging
import six

from xblock.core import XBlock
from xblock.fields import Dict, Scope, String
from web_fragments.fragment import Fragment
from webob import Response
from xblockutils.studio_editable import StudioEditableXBlockMixin


log = logging.getLogger(__name__)


def _(text):
    """
    A noop underscore function that marks strings for extraction.
    """
    return text


class SimulationXBlock(XBlock, StudioEditableXBlockMixin):
    """
    XBlock for simulations.
    """

    display_name = String(
        display_name=_('Display Name'),
        help=_('The display name for this component.'),
        default='Simulation',
        scope=Scope.content,
    )

    simulation_url = String(
        display_name=_('Simulation URL'),
        default='',
        help=_(
            'The URL of the simulation. Must end with forward slash.'
        ),
        scope=Scope.content,
    )

    simulation_init_function = String(
        display_name=_('Init function'),
        default='',
        help=_(
            'The name of the init function. It should be a global and will be called when the XBlock is loaded.'
        ),
        scope=Scope.content,
    )

    user_state = Dict(
        display_name=_('User State'),
        help=_('Field to store state for user.'),
        default={},
        scope=Scope.user_state,
    )

    editable_fields = ('display_name', 'simulation_url', 'simulation_init_function')

    has_author_view = True  # Tells Studio to use author_view

    def student_view(self, _context=None):
        """
        Renders student view for LMS.
        """
        fragment = Fragment()
        fragment.add_content(six.text_type(
            u'<div class="simulation-content"></div>'
        ))

        fragment.add_css_url(self.runtime.local_resource_url(self, 'public/css/simulation-xblock.css'))
        fragment.add_javascript_url(self.runtime.local_resource_url(self, 'public/js/simulation-xblock.js'))

        if self.simulation_url:
            fragment.add_css_url(self.simulation_url + 'main.css')
            fragment.add_javascript_url(self.simulation_url + 'main.js')

        json_args = {
            'initFunction': self.simulation_init_function,
            'userState': self.user_state,
            'getUserStateUrl': self.runtime.handler_url(self, 'get_user_state', '').rstrip('?'),
            'updateUserStateUrl': self.runtime.handler_url(self, 'update_user_state', '').rstrip('?'),
        }
        fragment.initialize_js('SimulationXBlockStudentView', json_args)

        return fragment

    def author_view(self, context=None):
        """
        Renders author view for Studio.
        """
        return self.student_view(context)

    @XBlock.handler
    def get_user_state(self, _request, _suffix=''):
        return Response(
            json.dumps(self.user_state),
            content_type='application/json',
            charset='UTF-8'
        )

    @XBlock.json_handler
    def update_user_state(self, data, _dispatch):
        self.user_state = data
        return self.user_state
