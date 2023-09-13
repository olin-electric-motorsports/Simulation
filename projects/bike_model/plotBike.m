function plotBike(simulateBike)
    wheels = simulateBike.wheels;
    velocities = simulateBike.velocities;
    ax = simulateBike.ax;
    ay = simualteBike.ay;


    figure()
    hold on
    plot(wheels(:,1),wheels(:,2), "g.")
    plot(wheels(:,3), wheels(:,4), 'r.')
    %quiver(wheels(:,1),wheels(:,2), velocities(:,1),velocities(:,2))
    quiver((wheels(:,1) + wheels(:,3))/2,(wheels(:,2) + wheels(:,4))/2, ax(:),ay(:),.5)
    %bike frame
    %plot([wheels(:,1),wheels(:,3)],[wheels(:,2), wheels(:,4)])
    q = quiver(wheels(:,3),wheels(:,4), -wheels(:,3) + wheels(:,1),-wheels(:,4)+wheels(:,2),'off');
    q.ShowArrowHead = 'off';

    %x vs y
    xlabel('x position of bicycle (m)')
    ylabel('y position of bicycle (m)')
    title('Path of a bicycle through space')
    legend('Front wheel','Back Wheel','Accelaration Vector')​
    ​
    hold off
    figure()
    plot(zout(:,1),zout(:,3));
    xlabel('x position of bicycle (m)')
    ylabel('y position of bicycle (m)')
    title('Path of a bicycle through space')
    legend('Path')

    %t vs x
    figure()
    plot(t,zout(:,1))
    xlabel('Simulation Time (s)')
    ylabel('X Position of Bicycle (m)')
    title('Bicycle X Position vs Time')
    legend('Bicycle Position')
    figure()

    % t vs omega
    plot(t,zout(:,6))
    xlabel('Simulation Time (s)')
    ylabel('Angular Velocity of the Bicycle (rad/s)')
    title('Bicycle Angular Velocity vs Time')
    legend('Bicycle Angular Velocity')
    figure()

    % t vs omega
    plot(t,zout(:,5))
    xlabel('Simulation Time (s)')
    ylabel('Angular Position of the Bicycle (rad)')
    title('Bicycle Angular Position vs Time')
    legend('Bicycle Angular Position')
end