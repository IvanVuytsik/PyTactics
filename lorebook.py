from settings import *
from importCSV import *
from lorebook_data import INFO, DOMAIN


class Lorebook:
    def __init__(self):
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SM)
        self.image = UI_ElEMENTS["lorebook"]
        self.rect = self.image.get_rect()
        self.selected_chapter = None

        self.display_surface = pygame.display.get_surface()
        self.full_width = self.display_surface.get_size()[0]
        self.full_height = self.display_surface.get_size()[1]

        self.rect.x = self.full_width * 0.15
        self.rect.y = self.full_height * 0.1

        self.total_chapters = len(DOMAIN)
        self.chapter_names = DOMAIN
        self.info = list(INFO.keys())
        self.info_data = list(INFO.values())

        self.chapter_list = self.create_chapters()
        self.info_lists = self.create_info_lists()
        #self.create_quests(self.chapter_names[0])

    def create_chapters(self):
        chapter_list = []
        for index, name in enumerate(DOMAIN):
            chapter = Chapter(self.rect.x + DOUBLETILE + (index * TRIPLETILE),
                              self.rect.y - TILESIZE, name)
            chapter_list.append(chapter)
        return chapter_list

    def create_info_lists(self):
        info_list = []
        for index, chapter in enumerate(self.chapter_names):
            new_list = self.create_info(self.chapter_names[index])
            info_list.append(new_list)
        return info_list

    def create_info(self, chapter):
        info_list = []
        n = -1
        for index, quest in enumerate(INFO): #[:10]
            if INFO[quest]["chapter"] == chapter:
                n += 1
                new_quest = Info(self.display_surface, quest, INFO[quest]["chapter"], self.rect.x + DOUBLETILE,
                                  self.rect.y + DOUBLETILE + (n * TILESIZE))
                info_list.append(new_quest)
        return info_list

    @staticmethod
    def deselect(chapter):
        if chapter.selected:
            chapter.selected = False
            chapter.rect.y += HALFTILE

    def chapter_input(self, input_metadata):
        for index, chapter in enumerate(self.chapter_list):
            if all([chapter.rect.collidepoint(input_metadata[2]), not self.rect.collidepoint(input_metadata[2]),
                    input_metadata[0], not chapter.selected]):
                for item in self.chapter_list:
                    self.deselect(item)
                time.sleep(0.1)
                chapter.selected = True
                chapter.rect.y -= HALFTILE
                sound_manager(SOUND_BANK["page"])
                self.selected_chapter = index
            elif all([chapter.rect.collidepoint(input_metadata[2]), not self.rect.collidepoint(input_metadata[2]),
                      input_metadata[0], chapter.selected]):
                time.sleep(0.1)
                chapter.selected = False
                chapter.rect.y += HALFTILE
                self.selected_chapter = None

    def info_input(self, input_metadata, selected_chapter):
        if self.selected_chapter is not None:
            for index, quest in enumerate(self.info_lists[selected_chapter]):
                if all([quest.rect.collidepoint(input_metadata[2]), input_metadata[0], not quest.selected]):
                    for item in self.info_lists[selected_chapter]:
                        item.selected = False
                    time.sleep(0.1)
                    quest.selected = True
                    sound_manager(SOUND_BANK["take"])
                elif all([quest.rect.collidepoint(input_metadata[2]), input_metadata[0], not quest.selected]):
                    time.sleep(0.1)
                    quest.selected = False

    def show_chapters(self):
        for index, chapter in enumerate(self.chapter_list):
            chapter.draw(self.display_surface, index)

    def show_chapter_data(self):
        for chapter in self.chapter_list:
            if chapter.selected:
                show_info(self.display_surface, chapter.name, chapter.chapter_font, BOOK_COLOR,
                          self.rect.x + FOURTILES, self.rect.y + QUARTERTILE)

    def show_info_per_chapter(self, input_metadata):
        for index in range(self.total_chapters):
            match self.selected_chapter:
                case index: self.show_info(index)
            self.info_input(input_metadata, index)

    def show_info(self, selected_chapter):
        if self.selected_chapter is not None:
            for index, info in enumerate(self.info_lists[selected_chapter]):
                if INFO[info.info_name]["status"] == "unlocked":
                    info.draw()

    def update(self, input_metadata):
        self.chapter_input(input_metadata)
        self.show_chapters()
        self.display_surface.blit(self.image, self.rect)
        self.show_chapter_data()
        self.show_info_per_chapter(input_metadata)


class Chapter:
    def __init__(self, x, y, name):
        self.selected = False
        self.name = name
        self.image = UI_ElEMENTS["booksection"]
        self.rect = self.image.get_rect()
        self.chapter_font = pygame.font.Font(UI_FONT, UI_FONT_MD)
        self.rect.x, self.rect.y = x, y

    def draw(self, display_surface, number):
        display_surface.blit(self.image, self.rect)
        show_info(display_surface, number, self.chapter_font, BOOK_COLOR,
                  self.rect.centerx - 5, self.rect.y + QUARTERTILE)
        # pygame.draw.rect(display_surface, (255, 0, 0), self.rect, 3)


class Info:
    def __init__(self, display_surface, info_name, quest_chapter, x, y):
        self.display_surface = display_surface
        self.full_width = display_surface.get_size()[0]
        self.full_height = display_surface.get_size()[1]
        self.selected = False
        self.quest_chapter = quest_chapter
        self.info_name = info_name
        self.image = INFO[info_name]["image"]
        self.description = INFO[info_name]["desc"]
        self.status = INFO[info_name]["status"]
        self.info_font = pygame.font.Font(TEXT_FONT, TEXT_FONT_MD)
        self.info_desc_font = pygame.font.Font(DESC_FONT, DESC_FONT_Mini)
        self.rect = pygame.rect.Rect(x, y, FOURTILES * 2, TILESIZE)
        self.x_static = self.full_width * 0.54
        self.y_static = self.full_height * 0.16
        #create image data if there is an image
        if self.image is not None:
            self.image_rect = self.image.get_rect()
            self.image_rect.x = self.x_static
            self.image_rect.y = self.y_static + HALFTILE
            self.start_line = self.image_rect.height
        else:
            self.start_line = 0

    def draw(self):
        show_info(self.display_surface, self.info_name, self.info_font,
                  BOOK_COLOR if not self.selected else LORE_COLOR,
                  self.rect.x, self.rect.y)
        # draw image and description
        if self.selected:
            if self.image is not None:
                self.display_surface.blit(self.image, self.image_rect)
                pygame.draw.rect(self.display_surface, "#bd754a", self.image_rect, 6)
            draw_story(self.display_surface, self.description, self.info_desc_font,
                       self.x_static, self.y_static + self.start_line, SEMITILE)
        # pygame.draw.rect(display_surface, (255, 0, 0), self.rect, 3)