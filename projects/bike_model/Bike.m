classdef Bike
    % A simple model of a Two-Wheeled Bicycle
    properties
        mass
        length
        inertia
        maxForce
        steerAngle
        timeSpan
        initialConditions

        weight
        radius
        cross_area
        gear_ratio
        
        velocity
        position
        angular_velocity
        torque_motor
    end
    properties (Constant)
        coeff_drag = 0.56
        coeff_rr = 0.002 % for bicycles
        rho = 1.225
        moment_inertia_yaw =0.5
        gravity = 9.8
    end
    properties (Dependent)
        drag_force
        normal_force
        tractive_force
        rr_force
        bikeMotion
    end

    methods
        function BikeObject = Bike(mass,length, inertia, maxForce,steerAngle,timeSpan,initialConditions)
            BikeObject.mass = mass;
            BikeObject.length = length;
            BikeObject.inertia = inertia;
            BikeObject.maxForce = maxForce;
            BikeObject.steerAngle = steerAngle;
            BikeObject.timeSpan = timeSpan;
            BikeObject.initialConditions = initialConditions;
        end

        function normal_force = get.normal_force(BikeObject)
            normal_force = 0.7*BikeObject.gravity*BikeObject.mass;
        end

        function drag_force = get.drag_force(BikeObject)
            drag_force = 0.5*BikeObject.coeff_drag*BikeObject.rho*BikeObject.cross_area*BikeObject.velocity^2;
        end

        function rr_force = get.rr_force(BikeObject)
            rr_force = BikeObject.coeff_rr*BikeObject.normal_force;
        end

        function bikeMotion = get.bikeMotion(BikeObject)
            Z = BikeObject.initialConditions
            length_bike = BikeObject.length;
            steer_angle = BikeObject.steerAngle;
            inertia_bike = BikeObject.inertia;
            mass_bike = BikeObject.mass;

            %Z(1) = x, z(2) = vx, Z(3) = y, Z(4) = vy, z(5) = theta_b, z(6) = omega_b
            %all in relation to COM​
            theta_b = Z(5);
            omega_b = Z(6);
            %in terms of i and j
            v_x_front = Z(2) + length_bike/2 * omega_b*(-sin(theta_b));
            v_y_front = Z(4) + length_bike/2 * omega_b*(cos(theta_b));
            %range of atan 2 -pi ->pi
            theta_slip_2 = atan2(v_y_front*cos(theta_b + steer_angle) -v_x_front*sin(theta_b+steer_angle),...
                            v_x_front*cos(theta_b + steer_angle) + v_y_front*sin(theta_b + steer_angle));
            v_x_back = Z(2) - length_bike/2 * omega_b*(-sin(theta_b));
            v_y_back = Z(4) - length_bike/2 * omega_b*(cos(theta_b));
            %range of atan 2 -pi ->pi
            theta_slip_1 = atan2(v_y_back*cos(theta_b) -v_x_back*sin(theta_b),...
                            v_x_back*cos(theta_b) + v_y_back*sin(theta_b));
            Force1 = Bike.ForceOutput(theta_slip_1);
            Force2 = Bike.ForceOutput(theta_slip_2);
            ax = (- Force1 * sin(theta_b) - Force2 * sin(theta_b + steer_angle))/mass_bike;
            ay = (Force1 * cos(theta_b) + Force2 * cos(theta_b + steer_angle))/mass_bike;
            alpha = (-length_bike/2 * Force1 + length_bike/2 *Force2 *sin(steer_angle + pi))/inertia_bike;
                        
                        
            dz1dt = Z(2); 
            dz2dt = ax;
            dz3dt = Z(4);
            dz4dt = ay;
            dz5dt = Z(6);
            dz6dt = alpha;
            dzdt = [dz1dt;dz2dt;dz3dt;dz4dt;dz5dt;dz6dt];

            bikeMotion = ode45(dzdt,BikeObject.timeSpan,BikeObject.initialConditions);
        end
        function simulateBike = simulateBike(BikeObject)
            [timestep, zout] = BikeObject.bikeMotion;

            step = 10;
            t_end = 30 * step;
            for i = step:step:t_end
                theta_b = zout(i,5);
                omega_b = zout(i,6);
                x_front((i/step)) = zout(i,1) + length_bike/2*(cos(theta_b));
                y_front(i/step) = zout(i,3) + length_bike/2*(sin(theta_b));
                x_back(i/step) = zout(i,1) - length_bike/2*(cos(theta_b));
                y_back(i/step) = zout(i,3) - length_bike/2*(sin(theta_b));
                
                
                v_x_front(i/step) = zout(i,2) + length_bike/2 * omega_b*(-sin(theta_b));
                v_y_front(i/step) = zout(i,4) + length_bike/2 * omega_b*(cos(theta_b));
                %range of atan 2 -pi ->pi
                theta_slip_2 = atan2(v_y_front(i/step)*cos(theta_b + steer_angle) -v_x_front(i/step)*sin(theta_b+steer_angle),...
                v_x_front(i/step)*cos(theta_b + steer_angle) + v_y_front(i/step)*sin(theta_b + steer_angle));
                v_x_back(i/step) = zout(i,2) - length_bike/2 * omega_b*(-sin(theta_b));
                v_y_back(i/step) = zout(i,4) - length_bike/2 * omega_b*(cos(theta_b));
                %range of atan 2 -pi ->pi
                theta_slip_1 = atan2(v_y_back(i/step)*cos(theta_b) -v_x_back(i/step)*sin(theta_b),...
                            v_x_back(i/step)*cos(theta_b) + v_y_back(i/step)*sin(theta_b));
                Force1 = Bike.ForceOutput(theta_slip_1);
                Force2 = Bike.ForceOutput(theta_slip_2);
                ax(i/step) = (- Force1 * sin(theta_b) - Force2 * sin(theta_b + steer_angle))/mass_bike;
                ay(i/step) = (Force1 * cos(theta_b) + Force2 * cos(theta_b + steer_angle))/mass_bike;
            end
            wheels = [x_front;y_front;x_back;y_back]';
            velocities = [v_x_front; v_y_front; v_x_back;v_y_back]';
            simulateBike = [wheels,velocities,ax,ay,timestep];
        end
    end
    methods(Static)
        function outp = ForceOutput(slip_angle)
            thresh = 15/360 *2*pi;
            if slip_angle < -thresh
                outp = BikeObject.maxForce;
            elseif slip_angle >= thresh
                outp = -(slip_angle*BikeObject.maxForce/thresh);
            elseif slip_angle > -thresh && slip_angle <= thresh
                outp = 0;
            end
            if slip_angle > thresh
                outp = -BikeObject.maxForce;
            end
        end
    end
end
