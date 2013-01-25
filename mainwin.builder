<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <!-- interface-requires gtk+ 3.0 -->
  <object class="GtkWindow" id="window1">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
    <property name="events">GDK_KEY_PRESS_MASK | GDK_KEY_RELEASE_MASK | GDK_STRUCTURE_MASK</property>
    <signal name="destroy" handler="cbquit" swapped="no"/>
    <signal name="key-press-event" handler="cbfancykeys" swapped="no"/>
    <child>
      <object class="GtkVBox" id="box1">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <child>
          <object class="GtkHBox" id="box4">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="valign">start</property>
            <child>
              <object class="GtkToggleButton" id="unratedview">
                <property name="label" translatable="yes">unrated</property>
                <property name="use_action_appearance">False</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
                <signal name="toggled" handler="cbchangedfilter" swapped="no"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkToggleButton" id="5starview">
                <property name="label" translatable="yes">3+star</property>
                <property name="use_action_appearance">False</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
                <signal name="toggled" handler="cbchangedfilter" swapped="no"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkToggleButton" id="hiddenview">
                <property name="label" translatable="yes">hidden</property>
                <property name="use_action_appearance">False</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
                <signal name="toggled" handler="cbchangedfilter" swapped="no"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkEntry" id="entry2">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="invisible_char">•</property>
                <property name="invisible_char_set">True</property>
                <property name="placeholder_text">search</property>
                <signal name="changed" handler="cbsearch" swapped="no"/>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="pack_type">end</property>
                <property name="position">3</property>
              </packing>
            </child>
            <child>
              <object class="GtkToggleButton" id="trashview">
                <property name="label" translatable="yes">trash</property>
                <property name="use_action_appearance">False</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
                <signal name="toggled" handler="cbchangedfilter" swapped="no"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">4</property>
              </packing>
            </child>
            <child>
              <object class="GtkToggleButton" id="versionedview">
                <property name="label" translatable="yes">versioned</property>
                <property name="use_action_appearance">False</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
                <signal name="toggled" handler="cbchangedfilter" swapped="no"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">5</property>
              </packing>
            </child>
            <child>
              <placeholder/>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkHBox" id="box2">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkDrawingArea" id="drawingarea1">
                <property name="visible">True</property>
                <property name="app_paintable">True</property>
                <property name="can_focus">True</property>
                <property name="has_focus">True</property>
                <property name="events">GDK_EXPOSURE_MASK | GDK_POINTER_MOTION_MASK | GDK_BUTTON_PRESS_MASK | GDK_BUTTON_RELEASE_MASK | GDK_STRUCTURE_MASK | GDK_SCROLL_MASK</property>
                <signal name="button-press-event" handler="cbclickedthumba" swapped="no"/>
                <signal name="configure-event" handler="cbredraw" swapped="no"/>
                <signal name="button-release-event" handler="cbclickedthumb" swapped="no"/>
                <signal name="key-press-event" handler="cbpressedkeymain" swapped="no"/>
                <signal name="scroll-event" handler="cbscroll" swapped="no"/>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkVScrollbar" id="scrollbar1">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <signal name="value-changed" handler="cbscrolledbar" swapped="no"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkHBox" id="box3">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkButton" id="button1">
                <property name="label" translatable="yes">button</property>
                <property name="use_action_appearance">False</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="button2">
                <property name="label" translatable="yes">button</property>
                <property name="use_action_appearance">False</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="button3">
                <property name="label" translatable="yes">button</property>
                <property name="use_action_appearance">False</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">2</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="currenteditor">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">editor</property>
                <property name="width_chars">19</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">3</property>
              </packing>
            </child>
            <child>
              <object class="GtkLabel" id="takentime">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">taken time</property>
                <property name="width_chars">19</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="position">4</property>
              </packing>
            </child>
            <child>
              <object class="GtkEntry" id="entry1">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="events">GDK_KEY_PRESS_MASK | GDK_KEY_RELEASE_MASK | GDK_STRUCTURE_MASK</property>
                <property name="invisible_char">•</property>
                <property name="invisible_char_set">True</property>
                <property name="secondary_icon_stock">gtk-apply</property>
                <signal name="key-release-event" handler="cbpressedkeycomment" swapped="no"/>
                <signal name="icon-press" handler="cbchangedcomment" swapped="no"/>
                <signal name="editing-done" handler="cbchangedcomment" swapped="no"/>
              </object>
              <packing>
                <property name="expand">True</property>
                <property name="fill">True</property>
                <property name="position">5</property>
              </packing>
            </child>
            <child>
              <object class="GtkToggleButton" id="overwritebutton">
                <property name="label" translatable="yes">overwrite</property>
                <property name="use_action_appearance">False</property>
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="use_action_appearance">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">6</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
