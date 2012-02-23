import sublime
import sublime_plugin
import re


class TagCloseTagOnSlashCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        for region in self.view.sel():
            cursorPosition = region.begin()
            previousCharacter = self.view.substr(sublime.Region(cursorPosition - 1, cursorPosition))

            if '<' == previousCharacter and self.view.score_selector(cursorPosition, 'text.html | text.xml') > 0:
                syntax = self.view.syntax_name(region.begin())
                should_skip = re.match(".*string.quoted.double", syntax) or re.match(".*string.quoted.single", syntax)

                if not should_skip:
                    # found match, run close_tag here
                    self.view.run_command('close_tag')

                    if self.view.sel()[0].begin() != cursorPosition:
                        # close_tag completed, so remove the extra angle bracket
                        self.view.erase(edit, sublime.Region(cursorPosition - 1, cursorPosition))
                    else:
                        # we need to insert a slash
                        self.view.insert(edit, cursorPosition, '/')

                else:
                    if region.empty():
                        self.view.insert(edit, cursorPosition, '/')
                    else:
                        self.view.replace(edit, sublime.Region(region.begin(), region.end()), '/')

            else:
                if region.empty():
                    self.view.insert(edit, cursorPosition, '/')
                else:
                    self.view.replace(edit, sublime.Region(region.begin(), region.end()), '/')

