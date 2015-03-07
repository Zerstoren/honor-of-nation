<div class="mpi__footer">
    <div class="mpi__selected_screen ui"></div>
    <div class="mpi__minimap ui"></div>
    <div class="mpi__selected_info ui">
        <div class="menu_interface">
            <div class="left">
                <div class="cursor_position">{{this.footer.x}} x {{this.footer.y}}</div>

                {{#this.footer.type == 'town'}}
                <div class="towns">
                    <div class="type">
                        {{#this.footer.town.type == 0}}
                        Село
                        {{/this.footer.town.type}}

                        {{#this.footer.town.type == 1}}
                        Город
                        {{/this.footer.town.type}}

                        {{#this.footer.town.type == 2}}
                        Замок
                        {{/this.footer.town.type}}

                        - {{this.footer.town.name}}
                    </div>
                    <div class="holder">Владелец: <a href="javascript:void(0)">Zerst</a></div>
                    <div class="population">
                        Население: {{formatters.transformNumberToPretty(this.footer.town.population)}}
                    </div>
                </div>
                {{/this.footer.type}}

                {{#this.footer.type == 'resource'}}
                <div class="resource">
                    <div class="type">
                        {{#this.footer.resource.type == 'rubins'}}
                        Рубиновая шахта
                        {{/this.footer.resource.type}}

                        {{#this.footer.resource.type == 'steel'}}
                        Рудная шахта
                        {{/this.footer.resource.type}}

                        {{#this.footer.resource.type == 'stone'}}
                        Каменный карьер
                        {{/this.footer.resource.type}}

                        {{#this.footer.resource.type == 'wood'}}
                        Лесопосадка
                        {{/this.footer.resource.type}}

                        {{#this.footer.resource.type == 'eat'}}
                        Родючие поля
                        {{/this.footer.resource.type}}
                    </div>

                    <div class="holder">Владелец:

                        {{#this.footer.resource.user != null}}
                            <a href="javascript:void(0)" data-id="{{this.footer.resource.user._id}}">
                                {{this.footer.resource.user.login}}
                            </a>
                        {{/this.footer.resource.user}}
                        {{^this.footer.resource.user}}
                            отсутствует
                        {{/this.footer.resource.user}}
                    </div>

                    {{#this.footer.resource.amount}}
                    <div class="amount">
                        <span data-hint="{{formatters.transformNumberToView(this.footer.resource.amount)}}">
                            Остаток: {{formatters.transformNumberToPretty(this.footer.resource.amount)}}
                        </span>
                    </div>
                    {{/this.footer.resource.amount}}

                    {{#this.footer.resource.output}}
                    <div class="base_output">
                        <span data-hint="{{formatters.transformNumberToView(this.footer.resource.output)}}">
                            Добыча: {{formatters.transformNumberToPretty(this.footer.resource.output)}}
                        </span>
                    </div>
                    {{/this.footer.resource.output}}
                </div>
                {{/this.footer.type}}

                {{#this.footer.type === 'army'}}
                <div class="army">
                    <img src="" />
                </div>
                {{/this.footer.type}}

            </div>

            <div class="right">
                {{#this.footer.type === 'army'}}
                <div class="army">
                    <div class="army_size">Размер армии: {{this.footer.army.count}}</div>
                    <div class="army_power">Запас сил: {{this.footer.army_power}}</div>
                    <div class="army_mode">
                        <button class="btn btn-default mode{{#this.footer.army.mode == 1}} active{{/this.footer.army.mode}}" data-mode="1"
                                data-hint="Медленное движение">I</button>
                        <button class="btn btn-default mode{{#this.footer.army.mode == 2}} active{{/this.footer.army.mode}}" data-mode="2"
                                data-hint="Нормальная скорость движения">II</button>
                        <button class="btn btn-default mode{{#this.footer.army.mode == 3}} active{{/this.footer.army.mode}}" data-mode="3"
                                data-hint="Быстрое движение">III</button>
                        <button class="btn btn-default mode{{#this.footer.army.mode == 4}} active{{/this.footer.army.mode}}" data-mode="4"
                                data-hint="Очень быстрое движение">IV</button>
                    </div>
                    {{#this.footer.time_to_complete}}
                    <div class="army_move">
                        движение через: {{formatters.fromIntToTime(this.footer.time_to_complete)}}
                    </div>
                    {{/this.footer.time_to_complete}}
                </div>
                {{/this.footer.type}}
            </div>

            <div class="center">

            </div>
        </div>
    </div>
</div>